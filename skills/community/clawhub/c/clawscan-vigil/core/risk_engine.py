"""
Risk Engine - Calculate overall risk score and level
"""

from typing import List
from core.models import Finding, RiskLevel, ScanResult


class RiskEngine:
    """
    Calculate overall risk based on findings.
    
    Risk calculation factors:
    - Severity of findings (HIGH=10, MEDIUM=3, LOW=1)
    - Confidence of findings
    - Category diversity (multiple categories = higher risk)
    """
    
    SEVERITY_WEIGHTS = {
        RiskLevel.HIGH: 10,
        RiskLevel.MEDIUM: 3,
        RiskLevel.LOW: 1,
        RiskLevel.UNKNOWN: 0,
    }
    
    # Categories that are immediate red flags
    CRITICAL_CATEGORIES = {
        "crypto_wallet",
        "dynamic_crypto",
        "code_execution",  # eval/exec
    }
    
    def calculate(self, findings: List[Finding], skill_name: str) -> RiskLevel:
        """
        Calculate overall risk level based on findings.
        """
        if not findings:
            return RiskLevel.LOW
        
        # Critical category check - immediate HIGH
        categories = {f.category for f in findings}
        if categories.intersection(self.CRITICAL_CATEGORIES):
            return RiskLevel.HIGH
        
        # Calculate weighted score
        total_score = 0
        for finding in findings:
            weight = self.SEVERITY_WEIGHTS.get(finding.level, 0)
            adjusted = weight * finding.confidence
            total_score += adjusted
        
        # Diversity bonus - more categories = higher risk
        category_bonus = len(categories) * 2
        total_score += category_bonus
        
        # Determine risk level
        if total_score >= 20:
            return RiskLevel.HIGH
        elif total_score >= 8:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def generate_recommendations(self, result: ScanResult) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        categories = {f.category for f in result.findings}
        
        if "network" in categories or "dynamic_network" in categories:
            recommendations.append(
                "⚠️  This Skill can make network requests. Verify it only connects to expected endpoints."
            )
        
        if "filesystem_write" in categories or "dynamic_filesystem" in categories:
            recommendations.append(
                "⚠️  This Skill can write to your filesystem. Check it doesn't modify sensitive files."
            )
        
        if "subprocess" in categories or "dynamic_subprocess" in categories:
            recommendations.append(
                "🚨 This Skill can execute system commands. This is a significant security risk."
            )
        
        if "crypto_wallet" in categories or "dynamic_crypto" in categories:
            recommendations.append(
                "🚨 CRITICAL: This Skill accesses cryptocurrency/wallet functionality. "
                "It could steal your crypto assets. Extreme caution advised."
            )
        
        if "obfuscation" in categories:
            recommendations.append(
                "⚠️  Code obfuscation detected. Malicious Skills often hide their true behavior."
            )
        
        if "api_keys" in categories:
            recommendations.append(
                "ℹ️  This Skill handles API keys. Ensure it doesn't exfiltrate your credentials."
            )
        
        if not recommendations:
            if result.overall_risk == RiskLevel.LOW:
                recommendations.append(
                    "✅ No significant security risks detected. This Skill appears safe to use."
                )
            else:
                recommendations.append(
                    "ℹ️  Review the detailed findings above before installing this Skill."
                )
        
        return recommendations
