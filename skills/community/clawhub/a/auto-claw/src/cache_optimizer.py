"""
Cache Optimizer — WordPress 缓存策略优化引擎
支持多级缓存配置/命中率分析/自动调优
"""
import re
import json
import time
import hashlib
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class CacheConfig:
    """缓存配置"""
    cache_type: str = ""  # page / object / transient / opcode / browser / cdn
    enabled: bool = False
    ttl: int = 0  # seconds
    priority: int = 0
    
    # 配置
    settings: Dict[str, Any] = field(default_factory=dict)
    
    # 统计
    hits: int = 0
    misses: int = 0
    size_bytes: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

@dataclass
class CacheRecommendation:
    """缓存优化建议"""
    cache_type: str
    priority: int  # 1-5, 1=最高
    action: str  # enable / disable / tune / investigate
    current_state: str
    recommended_state: str
    expected_impact: str  # "预计提升 X% 页面速度"
    commands: List[str] = field(default_factory=list)

@dataclass
class CacheReport:
    """缓存报告"""
    site_url: str
    timestamp: str
    
    configs: Dict[str, CacheConfig] = field(default_factory=dict)
    recommendations: List[CacheRecommendation] = field(default_factory=list)
    
    total_hits: int = 0
    total_misses: int = 0
    
    @property
    def overall_hit_rate(self) -> float:
        total = self.total_hits + self.total_misses
        return self.total_hits / total if total > 0 else 0.0

class CacheOptimizer:
    """
    WordPress 缓存策略优化引擎
    
    功能：
    1. 检测当前缓存配置（WP Super Cache/W3TC/WP Rocket/Redis/Object Cache）
    2. 多级缓存策略（页面/对象/浏览器/Opcode/CDN）
    3. TTL优化建议
    4. 缓存命中率分析
    5. Nginx/Redis/WP-CLI配置命令生成
    6. 自动调优脚本
    """
    
    def __init__(self, site_url: str = "", web_root: str = ""):
        self.site_url = site_url
        self.web_root = web_root
        self.wp_cli = "/usr/local/bin/wp"
        self.php_bin = "/www/server/php/82/bin/php"
        self.configs: Dict[str, CacheConfig] = {}
        self._detect_current_cache()
    
    def _run_wp(self, args: str) -> Tuple[str, str, int]:
        if not self.web_root:
            return "", "", 1
        cmd = f"cd {self.web_root} && WP_CLI_PHP={self.php_bin} {self.wp_cli} --allow-root {args}"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    
    def _detect_current_cache(self):
        """检测当前缓存配置"""
        # WordPress对象缓存
        object_cache = CacheConfig(
            cache_type="object",
            enabled=False,
            settings={}
        )
        
        # WP-CLI检测
        out, err, _ = self._run_wp("config get WP_CACHE")
        if "true" in out.lower():
            object_cache.enabled = True
            object_cache.ttl = 3600
            self.configs["object_cache"] = object_cache
        
        # Redis检测
        out, err, _ = self._run_wp("eval 'echo extension_loaded(\"redis\") ? \"yes\" : \"no\";'")
        if "yes" in out.lower():
            redis_cache = CacheConfig(
                cache_type="redis",
                enabled=True,
                ttl=3600,
                settings={"extension": "phpredis"}
            )
            self.configs["redis"] = redis_cache
        
        # 页面缓存
        page_cache = CacheConfig(
            cache_type="page",
            enabled=False,
            settings={}
        )
        
        # 检测WP Super Cache
        out, _, _ = self._run_wp("plugin list --status=active --format=json")
        if out and "wp-super-cache" in out.lower():
            page_cache.enabled = True
            page_cache.cache_type = "wp-super-cache"
            page_cache.ttl = 3600
        
        # 检测WP Rocket
        if out and "wp-rocket" in out.lower():
            page_cache.enabled = True
            page_cache.cache_type = "wp-rocket"
            page_cache.ttl = 7200
        
        # 检测W3TC
        if out and "w3-total-cache" in out.lower():
            page_cache.enabled = True
            page_cache.cache_type = "w3tc"
            page_cache.ttl = 7200
        
        self.configs["page_cache"] = page_cache
        
        # 浏览器缓存
        browser_cache = CacheConfig(
            cache_type="browser",
            enabled=False,
            ttl=86400
        )
        
        # Nginx配置检测
        nginx_conf = "/www/server/nginx/conf/nginx.conf"
        try:
            with open(nginx_conf, 'r') as f:
                content = f.read()
                if "expires" in content:
                    browser_cache.enabled = True
        except:
            pass
        
        self.configs["browser_cache"] = browser_cache
        
        # Opcode缓存
        opcode_cache = CacheConfig(
            cache_type="opcode",
            enabled=False
        )
        
        out, _, _ = self._run_wp("eval 'echo json_encode([\"opcache\" => function_exists(\"opcache_get_status\") ? 1 : 0]);'")
        if out and "opcache" in out.lower():
            opcode_cache.enabled = True
            opcode_cache.ttl = 3600
        
        self.configs["opcode"] = opcode_cache
    
    def analyze_opcache(self) -> Dict[str, Any]:
        """分析OPcache状态"""
        if not self.web_root:
            return {}
        
        result = {
            "enabled": False,
            "memory_usage": {},
            "hits": 0,
            "misses": 0,
            "issues": []
        }
        
        out, _, _ = self._run_wp('eval \'if(function_exists("opcache_get_status")){ echo json_encode(opcache_get_status());}else{echo "{}";}\' 2>/dev/null')
        
        if out and out != "{}":
            try:
                data = json.loads(out)
                result["enabled"] = True
                
                memory = data.get("memory_usage", {})
                result["memory_usage"] = {
                    "used": memory.get("used_memory", 0),
                    "free": memory.get("free_memory", 0),
                    "wasted": memory.get("wasted_memory", 0)
                }
                
                result["hits"] = data.get("opcache_statistics", {}).get("num_hits", 0)
                result["misses"] = data.get("opcache_statistics", {}).get("num_misses", 0)
                
                # 问题
                wasted_pct = data.get("opcache_statistics", {}).get("wasted_memory_percentage", 0)
                if wasted_pct > 10:
                    result["issues"].append(f"OPcache浪费{wasted_pct:.1f}%内存，建议增大缓存或清理")
                
            except:
                pass
        
        if not result["enabled"]:
            result["issues"].append("OPcache未启用，影响PHP性能")
        
        return result
    
    def generate_wp_cli_commands(self) -> List[Dict[str, str]]:
        """生成WP-CLI优化命令"""
        cmds = []
        
        # Nginx FastCGI缓存（如果用Nginx）
        cmds.append({
            "action": "nginx_cache",
            "description": "启用Nginx FastCGI缓存",
            "cmd": "# 在 Nginx site config 中添加:\n# fastcgi_cache_path /var/cache/nginx levels=1:2 keys_zone=WORDPRESS:100m inactive=60m;\n# fastcgi_cache WORDPRESS;"
        })
        
        # WP Super Cache
        cmds.append({
            "action": "wp_super_cache",
            "description": "启用WP Super Cache",
            "cmd": f"{self.wp_cli} plugin install wp-super-cache --activate"
        })
        
        # Redis对象缓存
        cmds.append({
            "action": "redis_object_cache",
            "description": "安装Redis对象缓存",
            "cmd": f"{self.wp_cli} plugin install redis-cache --activate && {self.wp_cli} redis enable"
        })
        
        # 浏览器缓存头
        cmds.append({
            "action": "browser_cache_headers",
            "description": "配置浏览器缓存（添加到.htaccess或Nginx）",
            "cmd": '''# Apache (.htaccess):
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/jpg "access plus 1 month"
ExpiresByType image/webp "access plus 1 month"
ExpiresByType text/css "access plus 1 week"
ExpiresByType application/javascript "access plus 1 week"
</IfModule>

# Nginx:
location ~* \\.(jpg|jpeg|png|gif|webp|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}'''
        })
        
        # OPcache优化
        cmds.append({
            "action": "opcache_tune",
            "description": "OPcache优化参数",
            "cmd": '''# php.ini:
opcache.memory_consumption=256
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=20000
opcache.revalidate_freq=2
opcache.validate_timestamps=0'''
        })
        
        return cmds
    
    def generate_recommendations(self) -> List[CacheRecommendation]:
        """生成缓存优化建议"""
        recs = []
        
        # 页面缓存
        pc = self.configs.get("page_cache")
        if not pc or not pc.enabled:
            recs.append(CacheRecommendation(
                cache_type="page",
                priority=1,
                action="enable",
                current_state="未启用页面缓存",
                recommended_state="启用WP Super Cache或Nginx FastCGI缓存",
                expected_impact="预计提升50-80%页面加载速度",
                commands=[c["cmd"] for c in self.generate_wp_cli_commands() if c["action"] == "wp_super_cache"]
            ))
        
        # 对象缓存
        oc = self.configs.get("object_cache")
        redis = self.configs.get("redis")
        if redis and not redis.enabled:
            recs.append(CacheRecommendation(
                cache_type="object",
                priority=2,
                action="enable",
                current_state="Redis未启用",
                recommended_state="启用Redis对象缓存",
                expected_impact="预计减少70%数据库查询",
                commands=[c["cmd"] for c in self.generate_wp_cli_commands() if c["action"] == "redis_object_cache"]
            ))
        elif not oc or not oc.enabled:
            recs.append(CacheRecommendation(
                cache_type="object",
                priority=2,
                action="enable",
                current_state="对象缓存未启用",
                recommended_state="启用持久对象缓存",
                expected_impact="预计减少50%数据库查询"
            ))
        
        # 浏览器缓存
        bc = self.configs.get("browser_cache")
        if not bc or not bc.enabled:
            recs.append(CacheRecommendation(
                cache_type="browser",
                priority=3,
                action="enable",
                current_state="浏览器缓存未配置",
                recommended_state="配置静态资源缓存",
                expected_impact="预计减少重复访问的服务器请求",
                commands=[c["cmd"] for c in self.generate_wp_cli_commands() if c["action"] == "browser_cache_headers"]
            ))
        
        # Opcode
        opcache = self.configs.get("opcode")
        if not opcache or not opcache.enabled:
            recs.append(CacheRecommendation(
                cache_type="opcode",
                priority=4,
                action="enable",
                current_state="OPcache未启用",
                recommended_state="启用并优化OPcache",
                expected_impact="预计提升20-30% PHP执行速度",
                commands=[c["cmd"] for c in self.generate_wp_cli_commands() if c["action"] == "opcache_tune"]
            ))
        
        return recs
    
    def run_full_analysis(self) -> CacheReport:
        """运行完整缓存分析"""
        report = CacheReport(
            site_url=self.site_url,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        report.configs = self.configs
        report.recommendations = self.generate_recommendations()
        
        # 统计
        for cfg in self.configs.values():
            report.total_hits += cfg.hits
            report.total_misses += cfg.misses
        
        return report
    
    def generate_nginx_config_snippet(self) -> str:
        """生成Nginx配置片段"""
        return '''
# ===== Auto-Claw Cache Optimization =====
# 添加到 Nginx site configuration

# 上游PHP
upstream php_backend {
    server 127.0.0.1:9000;
}

# FastCGI缓存
fastcgi_cache_path /var/cache/nginx/wordpress levels=1:2 keys_zone=WORDPRESS:100m inactive=60m max_size=500m;
fastcgi_cache_key "$scheme$request_method$host$request_uri";
fastcgi_cache_use_stale error timeout updating http_500;

# 缓存响应头
add_header X-Cache-Status $upstream_cache_status always;

# WordPress缓存规则
set $skip_cache 0;
if ($request_method = POST) { set $skip_cache 1; }
if ($query_string != "") { set $skip_cache 1; }
if ($request_uri ~* "/wp-admin/|/wp-json/|/cart/|/checkout/|/my-account/") {
    set $skip_cache 1;
}

# 静态资源
location ~* \\.(jpg|jpeg|png|gif|webp|svg|ico|css|js|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}
'''

def demo():
    optimizer = CacheOptimizer(
        site_url="http://linghangyuan1234.dpdns.org",
        web_root="/www/wwwroot/linghangyuan1234.dpdns.org"
    )
    
    print("\n🔍 缓存配置检测结果:")
    for name, cfg in optimizer.configs.items():
        status = "✅ 已启用" if cfg.enabled else "❌ 未启用"
        print(f"   {name}: {status} (TTL: {cfg.ttl}s)")
    
    # 分析OPcache
    opcache = optimizer.analyze_opcache()
    if opcache.get("enabled"):
        print(f"\n   OPcache: ✅ 启用")
        if opcache.get("issues"):
            for issue in opcache["issues"][:2]:
                print(f"   ⚠️  {issue}")
    else:
        print(f"\n   OPcache: ❌ 未启用")
    
    # 生成建议
    recs = optimizer.generate_recommendations()
    
    print(f"\n📋 优化建议 ({len(recs)}项):")
    for rec in recs:
        icon = "🔴" if rec.priority <= 2 else "🟡" if rec.priority <= 3 else "🟢"
        print(f"   {icon} [{rec.cache_type}] {rec.action.upper()}")
        print(f"      当前: {rec.current_state}")
        print(f"      影响: {rec.expected_impact}")
    
    # WP-CLI命令
    cmds = optimizer.generate_wp_cli_commands()
    print(f"\n📝 WP-CLI命令 ({len(cmds)}条):")
    for c in cmds[:3]:
        print(f"   - {c['action']}: {c['description']}")

if __name__ == "__main__":
    demo()
