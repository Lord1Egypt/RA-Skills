"""
Curl Risk Classifier for Security Scanner v6.2.0

对 curl 命令进行三级风险分类:
- HIGH: 远程执行 + 未知域名 + 混淆
- MEDIUM: 静默执行 / 非标准动作 / 隐藏输出
- LOW: 常见操作 + 透明执行

用户规则:
1. curl | bash / pipe → HIGH
2. 未知域名 + 数据外发 → HIGH
3. 混淆编码 (Base64等) → HIGH
4. 后台静默下载 → MEDIUM
5. 隐藏输出 (2>&1 >/dev/null) → MEDIUM
6. 私有IP/localhost → MEDIUM
7. 常见域名 (github.com, pypi.org等) → LOW
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CurlRiskResult:
    level: str  # HIGH / MEDIUM / LOW / SAFE
    pattern: str  # 匹配到的具体模式
    reason: str  # 判定理由
    matched_content: str  # 匹配到的原始内容


class CurlRiskClassifier:
    """Curl 命令风险分级分类器"""
    
    # ========== 高危模式 ==========
    HIGH_RISK_PATTERNS = [
        # 远程下载直接执行
        (r'curl\s+.*?\|\s*(bash|sh|python|perl|ruby|node)\b', 
         'REMOTE_PIPE_EXEC', '远程下载通过管道直接执行'),
        
        # curl -d 数据外发到外部
        (r'curl\s+.*?(?:--data|-d)\s*.*?\@-\s*.*?https?://[^\s]*', 
         'DATA_EXFIL', '数据外发到未知服务器'),
        
        # curl + Base64 混淆
        (r'curl\s+.*?\|.*?(?:base64\s+-d|atob|decode)',
         'OBFUSCATED_DOWNLOAD', 'Base64混淆的远程下载'),
        
        # 隐藏的远程执行
        (r'(?:eval|exec)\s*\(.*?(?:curl|wget)\s+', 
         'HIDDEN_EXEC', '隐藏的远程代码执行'),
        
        # curl 配合反向shell
        (r'/dev/tcp/[^\s]+|bash\s+-i\s+>&.*/dev/',
         'REVERSE_SHELL', '反向Shell连接'),
        
        # 凭据外发
        (r'curl\s+.*?(?:\.json|\.config|credentials|api_key|token).*?https?://[^\s]*',
         'CRED_EXFIL', '凭据数据外发'),
        
        # 混淆的 C2 域名 (数字 IP、hex 域名等)
        (r'curl\s+.*?(?:0x[a-f0-9]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?/[^\s]*)',
         'C2_DOMAIN', '可疑C2域名或IP'),
        
        # 未知外部域名 (非白名单)
        (r'curl\s+.*?https?://(?!www\.google\.com|api\.github\.com|pypi\.org|npmjs\.com|docker\.com|kubernetes\.io|cloudflare\.com|cdnjs\.cloudflare\.com)[a-z0-9][a-z0-9-]*\.[a-z]{2,}(?::\d+)?/[^\s]*\|',
         'UNKNOWN_PIPE', '未知域名+管道执行'),
    ]
    
    # ========== 中危模式 ==========
    MEDIUM_RISK_PATTERNS = [
        # 静默下载
        (r'curl\s+.*?>\s*(?:/dev/null|/tmp/[^\s]+)\s*(?:&&|\|)',
         'SILENT_DOWNLOAD', '静默后台下载'),
        
        # 隐藏输出
        (r'curl\s+[^\s]*\s+2?\>&1\s*>\s*/dev/null',
         'HIDDEN_OUTPUT', '故意隐藏curl输出'),
        
        # 私有IP/内网
        (r'curl\s+.*?(?:10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+|192\.168\.\d+)\d*',
         'PRIVATE_IP', '访问内网IP'),
        
        # curl 后台执行
        (r'curl\s+.*?--background\b',
         'BACKGROUND_EXEC', '后台执行curl'),
        
        # curl 写入可执行目录
        (r'curl\s+.*?-o\s+(?:/tmp|/var/tmp|/root)',
         'WRITE_TO_TMP', '下载到可执行目录'),
        
        # wget 代替 curl
        (r'wget\s+.*?(?:-O\s+(?:/tmp|/root)|\|)',
         'WGET_SUSPICIOUS', 'wget可疑用法'),
        
        # curl 无用户告知 (静默)
        (r'curl\s+.*?-s\s+.*?(?:https?://[^\s]+)\s*(?:;|\&\&)',
         'SILENT_CURL', '静默curl无错误提示'),
    ]
    
    # ========== 低危模式 (白名单) ==========
    SAFE_DOMAINS = [
        'api.github.com',
        'github.com',
        'raw.githubusercontent.com',
        'pypi.org',
        'pipy.org',
        'npmjs.com',
        'registry.npmjs.org',
        'docker.com',
        'docker.io',
        'kubernetes.io',
        'cloudflare.com',
        'cdnjs.cloudflare.com',
        'jsdelivr.com',
        'unpkg.com',
        'puppeteer',
        'chromium.org',
        'google.com',
        'googleapis.com',
        'gstatic.com',
        'python.org',
        'ubuntu.com',
        'debian.org',
        'archlinux.org',
        'get.docker.com',
        'storage.googleapis.com',
        'cdn.jsdelivr.net',
        'registry.npmmirror.com',  # 淘宝npm镜像
        'registry.npm.taobao.org',  # 旧版淘宝npm
    ]
    
    def __init__(self):
        self._compile_regex()
    
    def _compile_regex(self):
        """预编译所有正则表达式"""
        self._high_patterns = [
            (re.compile(p, re.IGNORECASE | re.MULTILINE), name, desc)
            for p, name, desc in self.HIGH_RISK_PATTERNS
        ]
        self._medium_patterns = [
            (re.compile(p, re.IGNORECASE | re.MULTILINE), name, desc)
            for p, name, desc in self.MEDIUM_RISK_PATTERNS
        ]
    
    def _is_safe_domain(self, url: str) -> bool:
        """检查是否为白名单域名"""
        url_lower = url.lower()
        for safe in self.SAFE_DOMAINS:
            if safe in url_lower:
                return True
        return False
    
    def _extract_url_from_curl(self, curl_cmd: str) -> Optional[str]:
        """从 curl 命令中提取 URL"""
        # 匹配 curl ... URL ... 模式
        match = re.search(r'curl\s+[^\s]*\s+(https?://[^\s\'"]+)', curl_cmd, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # 匹配 curl URL 模式
        match = re.search(r'curl\s+(https?://[^\s\'"]+)', curl_cmd, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def classify_curl(self, content: str) -> List[CurlRiskResult]:
        """
        分析文本中的所有 curl 命令并返回分级结果列表
        
        返回: List[CurlRiskResult], 按风险等级从高到低排序
        """
        results = []
        
        # 查找所有 curl 命令 (可能跨行)
        curl_pattern = r'curl\s+[^\n]{10,}'
        for match in re.finditer(curl_pattern, content, re.IGNORECASE | re.MULTILINE):
            curl_cmd = match.group(0)
            
            # 提取URL
            url = self._extract_url_from_curl(curl_cmd)
            
            # 检查高危模式
            for pattern, name, desc in self._high_patterns:
                if pattern.search(curl_cmd):
                    # 如果有URL但属于白名单，降级为LOW
                    if url and self._is_safe_domain(url) and name == 'UNKNOWN_PIPE':
                        results.append(CurlRiskResult(
                            level='LOW',
                            pattern=name,
                            reason=f'{desc} (白名单域名: {url})',
                            matched_content=curl_cmd[:200]
                        ))
                    else:
                        results.append(CurlRiskResult(
                            level='HIGH',
                            pattern=name,
                            reason=desc,
                            matched_content=curl_cmd[:200]
                        ))
                    break  # 匹配到就跳出，避免重复
            else:
                # 检查中危模式
                for pattern, name, desc in self._medium_patterns:
                    if pattern.search(curl_cmd):
                        results.append(CurlRiskResult(
                            level='MEDIUM',
                            pattern=name,
                            reason=desc,
                            matched_content=curl_cmd[:200]
                        ))
                        break
                else:
                    # 未匹配任何模式，检查是否有URL
                    if url:
                        # 有URL但不在白名单 -> MEDIUM
                        if not self._is_safe_domain(url):
                            results.append(CurlRiskResult(
                                level='MEDIUM',
                                pattern='UNKNOWN_DOMAIN',
                                reason=f'访问非白名单域名: {url}',
                                matched_content=curl_cmd[:200]
                            ))
                        else:
                            # 白名单域名 -> LOW
                            results.append(CurlRiskResult(
                                level='LOW',
                                pattern='SAFE_CURL',
                                reason=f'白名单域名 (安全): {url}',
                                matched_content=curl_cmd[:200]
                            ))
                    else:
                        # 没有URL的curl命令 -> MEDIUM
                        results.append(CurlRiskResult(
                            level='MEDIUM',
                            pattern='CURL_NO_URL',
                            reason='curl命令但无法提取URL',
                            matched_content=curl_cmd[:200]
                        ))
        
        return results
    
    def get_highest_risk(self, content: str) -> CurlRiskResult:
        """获取最高的风险等级"""
        results = self.classify_curl(content)
        if not results:
            return None
        
        # 按风险等级排序
        level_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'SAFE': 3}
        results.sort(key=lambda x: level_order.get(x.level, 99))
        
        return results[0]
    
    def generate_report(self, content: str) -> Dict:
        """生成风险报告"""
        results = self.classify_curl(content)
        
        report = {
            'total_findings': len(results),
            'risk_summary': {
                'HIGH': sum(1 for r in results if r.level == 'HIGH'),
                'MEDIUM': sum(1 for r in results if r.level == 'MEDIUM'),
                'LOW': sum(1 for r in results if r.level == 'LOW'),
                'SAFE': sum(1 for r in results if r.level == 'SAFE'),
            },
            'findings': [
                {
                    'level': r.level,
                    'pattern': r.pattern,
                    'reason': r.reason,
                    'snippet': r.matched_content
                }
                for r in results
            ]
        }
        
        return report


# 单例实例
_curl_classifier = None

def get_curl_classifier() -> CurlRiskClassifier:
    """获取全局Curl分类器实例"""
    global _curl_classifier
    if _curl_classifier is None:
        _curl_classifier = CurlRiskClassifier()
    return _curl_classifier
