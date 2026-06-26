"""
Batch scanning functionality for Premium users
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from core.scanner import Scanner
from core.models import RiskLevel


console = Console()


class BatchScanner:
    """Scan multiple Skills in batch"""
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.results = []
    
    def find_skills(self) -> List[Path]:
        """Find all Skill directories"""
        skills = []
        
        if not self.skills_dir.exists():
            return skills
        
        for item in self.skills_dir.iterdir():
            if item.is_dir():
                # Check if it looks like a Skill (has SKILL.md or Python files)
                has_skill_md = (item / "SKILL.md").exists()
                has_python = list(item.glob("*.py"))
                
                if has_skill_md or has_python:
                    skills.append(item)
        
        return sorted(skills)
    
    def scan_all(self, verbose: bool = False) -> Dict:
        """Scan all found Skills"""
        skills = self.find_skills()
        
        if not skills:
            console.print("[yellow]No Skills found in {self.skills_dir}[/yellow]")
            return {"scanned": 0, "high_risk": 0, "medium_risk": 0, "low_risk": 0}
        
        console.print(f"[dim]Found {len(skills)} Skills to scan...[/dim]\n")
        
        scanner = Scanner()
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task = progress.add_task("Scanning...", total=len(skills))
            
            for skill_path in skills:
                progress.update(task, description=f"Scanning {skill_path.name}...")
                
                try:
                    result = scanner.scan_skill(skill_path, skill_path.name)
                    results.append(result)
                except Exception as e:
                    console.print(f"[red]Failed to scan {skill_path.name}: {e}[/red]")
                
                progress.advance(task)
        
        # Generate summary
        summary = self._generate_summary(results)
        self._print_summary_table(results)
        
        return summary
    
    def _generate_summary(self, results: List) -> Dict:
        """Generate summary statistics"""
        high = sum(1 for r in results if r.overall_risk == RiskLevel.HIGH)
        medium = sum(1 for r in results if r.overall_risk == RiskLevel.MEDIUM)
        low = sum(1 for r in results if r.overall_risk == RiskLevel.LOW)
        
        return {
            "scanned": len(results),
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _print_summary_table(self, results: List):
        """Print summary table"""
        table = Table(title="Batch Scan Results")
        table.add_column("Skill", style="cyan")
        table.add_column("Risk", style="bold")
        table.add_column("Findings", justify="right")
        table.add_column("Files", justify="right")
        
        for result in sorted(results, key=lambda r: r.overall_risk.value, reverse=True):
            risk_color = {
                RiskLevel.HIGH: "red",
                RiskLevel.MEDIUM: "yellow",
                RiskLevel.LOW: "green",
            }.get(result.overall_risk, "white")
            
            emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                result.overall_risk.value, "⚪"
            )
            
            table.add_row(
                result.skill_name,
                f"[{risk_color}]{emoji} {result.overall_risk.value.upper()}[/{risk_color}]",
                str(len(result.findings)),
                str(result.files_scanned),
            )
        
        console.print(table)
        
        # Print risk summary
        high = sum(1 for r in results if r.overall_risk == RiskLevel.HIGH)
        medium = sum(1 for r in results if r.overall_risk == RiskLevel.MEDIUM)
        low = sum(1 for r in results if r.overall_risk == RiskLevel.LOW)
        
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  🔴 High Risk: {high}")
        console.print(f"  🟡 Medium Risk: {medium}")
        console.print(f"  🟢 Low Risk: {low}")
        
        if high > 0:
            console.print(f"\n[red]⚠️  {high} Skills have HIGH risk - review recommended![/red]")
    
    def export_json(self, output_file: Path):
        """Export results to JSON"""
        data = {
            "scan_timestamp": datetime.now().isoformat(),
            "skills_dir": str(self.skills_dir),
            "results": [
                {
                    "skill": r.skill_name,
                    "risk": r.overall_risk.value,
                    "findings": len(r.findings),
                    "files": r.files_scanned,
                }
                for r in self.results
            ]
        }
        
        output_file.write_text(json.dumps(data, indent=2))
        console.print(f"\n[green]Results exported to: {output_file}[/green]")
