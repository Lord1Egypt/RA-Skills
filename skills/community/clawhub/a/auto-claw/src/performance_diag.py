"""
Performance Diagnostic — WordPress 性能诊断工具
Core Web Vitals / TTFB / LCP / CLS 分析与根因定位
"""
import re
import json
import time
import subprocess
import requests
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from urllib.parse import urlparse

@dataclass
class PageSpeedMetrics:
    """页面性能指标"""
    url: str = ""
    ttfb_ms: float = 0.0          # Time to First Byte
    fcp_ms: float = 0.0            # First Contentful Paint
    lcp_ms: float = 0.0            # Largest Contentful Paint
    fid_ms: float = 0.0             # First Input Delay
    cls_score: float = 0.0           # Cumulative Layout Shift
    tbt_ms: float = 0.0             # Total Blocking Time
    speed_index: float = 0.0
    
    # 评分
    performance_score: int = 0        # 0-100 Lighthouse分数
    
    # 设备
    is_mobile: bool = False
    is_desktop: bool = True
    
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class PerformanceReport:
    """完整性能报告"""
    site_url: str
    pages: List[PageSpeedMetrics] = field(default_factory=list)
    avg_score: float = 0.0
    critical_pages: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class PerformanceDiagnostic:
    """
    WordPress 性能诊断工具
    
    功能：
    1. 使用 Google PageSpeed API 检测 Core Web Vitals
    2. 测量 TTFB / LCP / CLS / FID
    3. PHP-FPM / MySQL / Nginx 状态检查
    4. 慢查询分析
    5. 插件性能影响分析
    6. 生成可执行的优化建议
    """
    
    def __init__(self, site_url: str, web_root: str = "", php_bin: str = "", wp_cli: str = "/usr/local/bin/wp"):
        self.site_url = site_url.rstrip("/")
        self.web_root = web_root
        self.php_bin = php_bin or "/www/server/php/82/bin/php"
        self.wp_cli = wp_cli
        self.session = requests.Session()
    
    def _wp(self, args: str) -> Tuple[str, str, int]:
        if not self.web_root:
            return "", "No web root", 1
        cmd = f"cd {self.web_root} && WP_CLI_PHP={self.php_bin} {self.wp_cli} --allow-root {args}"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    
    def measure_ttfb(self, url: str) -> float:
        """测量 TTFB (Time To First Byte)"""
        try:
            start = time.time()
            r = self.session.get(url, timeout=10, verify=False)
            ttfb = (time.time() - start) * 1000
            return ttfb
        except:
            return 0.0
    
    def check_php_fpm_status(self) -> Dict[str, Any]:
        """检查 PHP-FPM 状态"""
        if not self.web_root:
            return {"available": False}
        
        result = {
            "available": False,
            "status": {},
            "issues": []
        }
        
        # 尝试通过 Nginx status 页面
        try:
            r = self.session.get("http://127.0.0.1/status", timeout=5)
            if r.status_code == 200:
                result["available"] = True
                result["status"]["raw"] = r.text
        except:
            pass
        
        # PHP-FPM 命令检查
        out, err, _ = self._wp("eval 'echo json_encode([\"php_version\" => PHP_VERSION]);'")
        if out:
            result["php_version"] = out
        
        return result
    
    def check_slow_queries(self) -> Dict[str, Any]:
        """检查 MySQL 慢查询"""
        if not self.web_root:
            return {"available": False}
        
        result = {
            "slow_query_log_enabled": False,
            "slow_query_count": 0,
            "queries": [],
            "issues": []
        }
        
        # 检查慢查询日志
        out, err, _ = self._wp("db query \"SHOW VARIABLES LIKE 'slow_query_log'\" --format=json")
        if out and "ON" in out.upper():
            result["slow_query_log_enabled"] = True
        
        # WordPress 的查询监控（通过 WP-CLI）
        out, _, _ = self._wp("eval 'global $wpdb; $q = $wpdb->get_results(\"SHOW GLOBAL STATUS LIKE \\\"Slow_queries\\\"\", ARRAY_A); echo json_encode($q);' --skip-plugins --skip-themes 2>/dev/null || echo '{\"error\":\"N/A\"}'")
        
        return result
    
    def analyze_plugins_performance(self) -> List[Dict[str, Any]]:
        """分析插件性能影响"""
        if not self.web_root:
            return []
        
        plugins = []
        out, _, _ = self._wp("plugin list --status=active --format=json")
        if not out:
            return []
        
        try:
            active_plugins = json.loads(out)
            for p in active_plugins:
                plugins.append({
                    "name": p.get("name", ""),
                    "status": p.get("status", ""),
                    "update_available": p.get("update", "none") != "none",
                    "performance_flag": self._check_plugin_heavy(p.get("name", "")),
                })
        except:
            pass
        
        return plugins
    
    def _check_plugin_heavy(self, plugin_name: str) -> str:
        """估算插件性能开销"""
        # 已知的重型插件
        heavy_plugins = {
            "jetpack": "HIGH",
            "wp-rocket": "LOW",
            "w3tc": "MEDIUM",
            "elementor": "HIGH",
            "divi": "HIGH",
            "yoast": "LOW",
            "wordfence": "MEDIUM",
            "all-in-one-seo": "LOW",
            "contact-form-7": "LOW",
            "woocommerce": "HIGH",
        }
        
        name_lower = plugin_name.lower()
        for known, level in heavy_plugins.items():
            if known in name_lower:
                return level
        
        return "MEDIUM"  # 默认中等
    
    def check_object_cache(self) -> Dict[str, Any]:
        """检查对象缓存"""
        if not self.web_root:
            return {"available": False}
        
        result = {
            "has_redis": False,
            "has_memcached": False,
            "has_object_cache": False,
            "issues": []
        }
        
        # 检查 WP_CACHE
        out, _, _ = self._wp("config get WP_CACHE")
        if "true" in out.lower():
            result["has_object_cache"] = True
        
        # 检查 Redis 插件
        out, _, _ = self._wp("plugin list --status=active --format=json")
        if out and "redis" in out.lower():
            result["has_redis"] = True
        
        return result
    
    def check_core_web_vitals_api(self, url: str, api_key: str = "") -> PageSpeedMetrics:
        """使用 PageSpeed Insights API"""
        metrics = PageSpeedMetrics(url=url)
        
        if not api_key:
            # 使用本地测量作为替代
            metrics.ttfb_ms = self.measure_ttfb(url)  # Already returns ms
            metrics.performance_score = 80 if metrics.ttfb_ms < 500 else 60 if metrics.ttfb_ms < 1000 else 40
            return metrics
        
        try:
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}&strategy=mobile"
            r = self.session.get(api_url, timeout=30)
            data = r.json()
            
            lighthouse = data.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})
            
            # 提取指标
            metrics.performance_score = lighthouse.get("categories", {}).get("performance", {}).get("score", 0) * 100
            
            # TTFB
            ttfb = audits.get("server-response-time", {})
            metrics.ttfb_ms = ttfb.get("numericValue", 0)
            
            # LCP
            lcp = audits.get("largest-contentful-paint", {})
            metrics.lcp_ms = lcp.get("numericValue", 0)
            
            # CLS
            cls = audits.get("cumulative-layout-shift", {})
            metrics.cls_score = cls.get("numericValue", 0)
            
            # FCP
            fcp = audits.get("first-contentful-paint", {})
            metrics.fcp_ms = fcp.get("numericValue", 0)
            
        except Exception as e:
            metrics.issues.append(f"API测量失败: {e}")
        
        return metrics
    
    def run_full_diagnostic(self, api_key: str = "", max_pages: int = 5) -> PerformanceReport:
        """运行完整性能诊断"""
        print(f"🔍 开始性能诊断: {self.site_url}")
        
        report = PerformanceReport(site_url=self.site_url)
        
        # 1. 获取页面列表
        urls = [self.site_url]
        if self.web_root:
            out, _, _ = self._wp(f"post list --post_type=page --post_status=publish --posts_per_page={max_pages} --format=ids")
            for pid in out.strip().split():
                urls.append(f"{self.site_url}/?p={pid}")
        
        # 2. 测试每个页面
        for url in urls[:max_pages]:
            print(f"   测试: {url[:60]}...")
            m = self.check_core_web_vitals_api(url, api_key)
            report.pages.append(m)
            
            if m.performance_score < 60:
                report.critical_pages.append(url)
        
        # 3. 服务器诊断
        print("   检查 PHP-FPM...")
        php_status = self.check_php_fpm_status()
        
        print("   检查插件性能...")
        plugins = self.analyze_plugins_performance()
        
        print("   检查对象缓存...")
        cache = self.check_object_cache()
        
        # 4. 计算平均分
        if report.pages:
            report.avg_score = sum(p.performance_score for p in report.pages) / len(report.pages)
        
        # 5. 生成建议
        report.recommendations = self._generate_recommendations(
            report.pages, plugins, cache, php_status
        )
        
        return report
    
    def _generate_recommendations(self, pages, plugins, cache, php_status) -> List[str]:
        """生成性能优化建议"""
        recs = []
        
        # 基于页面评分
        if pages:
            avg = sum(p.performance_score for p in pages) / len(pages)
            if avg < 50:
                recs.append("🔴 性能评分严重偏低，建议立即优化")
            elif avg < 70:
                recs.append("🟡 性能有提升空间")
            else:
                recs.append("🟢 性能基本良好")
            
            # TTFB
            avg_ttfb = sum(p.ttfb_ms for p in pages) / len(pages)
            if avg_ttfb > 2000:
                recs.append(f"🔴 TTFB过高({avg_ttfb:.0f}ms)，建议: 启用CDN/缓存/优化服务器")
            elif avg_ttfb > 800:
                recs.append(f"🟡 TTFB偏高({avg_ttfb:.0f}ms)，建议优化数据库查询")
        
        # 插件
        heavy = [p for p in plugins if p.get("performance_flag") == "HIGH"]
        if heavy:
            names = ", ".join(p["name"] for p in heavy[:3])
            recs.append(f"⚠️ 检测到重型插件: {names}")
        
        # 缓存
        if not cache.get("has_object_cache"):
            recs.append("💾 建议启用对象缓存(Redis/Memcached)")
        
        if not cache.get("has_redis"):
            recs.append("📦 考虑使用Redis进行持久缓存")
        
        # PHP-FPM
        if php_status.get("issues"):
            for issue in php_status["issues"]:
                recs.append(f"⚠️ PHP-FPM: {issue}")
        
        if not recs:
            recs.append("✅ 未发现明显性能问题")
        
        return recs

def demo():
    diag = PerformanceDiagnostic(
        site_url="http://linghangyuan1234.dpdns.org",
        web_root="/www/wwwroot/linghangyuan1234.dpdns.org"
    )
    
    report = diag.run_full_diagnostic()
    
    print(f"\n📊 性能报告: {report.site_url}")
    print(f"   平均分: {report.avg_score:.0f}/100")
    print(f"   严重页面: {len(report.critical_pages)}")
    
    for p in report.pages:
        print(f"\n   {p.url}")
        print(f"   评分: {p.performance_score}/100 | TTFB: {p.ttfb_ms:.0f}ms")
    
    print("\n建议:")
    for r in report.recommendations:
        print(f"  {r}")

if __name__ == "__main__":
    demo()
