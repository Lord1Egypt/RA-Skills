"""
Image Optimizer — WordPress 图片自动优化工具
扫描未优化图片、自动压缩、生成响应式规格、添加WebP
"""
import os
import re
import json
import subprocess
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

@dataclass
class ImageInfo:
    """单张图片的分析结果"""
    path: str  # 服务器路径
    url: str
    width: int = 0
    height: int = 0
    size_bytes: int = 0
    size_kb: float = 0.0
    format: str = ""  # jpg/png/gif/webp
    
    # 优化分析
    is_optimized: bool = False
    compression_potential: float = 0.0  # 可压缩比例 0-1
    recommended_format: str = ""  # 建议格式
    issues: List[str] = field(default_factory=list)
    
    # 建议
    needs_webp: bool = False
    needs_lazy_load: bool = False
    needs_responsive: bool = False
    needs_alt_text: bool = False
    
    # 优化后的预期大小
    estimated_size_kb: float = 0.0
    savings_kb: float = 0.0

@dataclass
class ImageOptimizationReport:
    """整站图片优化报告"""
    site_url: str
    total_images: int = 0
    total_size_mb: float = 0.0
    optimized_size_mb: float = 0.0
    potential_savings_mb: float = 0.0
    images: List[ImageInfo] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class ImageOptimizer:
    """
    WordPress 图片自动优化工具
    
    功能：
    1. 扫描 WordPress 上传目录中的所有图片
    2. 分析每个图片的优化状态
    3. 识别问题（未压缩/无WebP/无alt/无响应式）
    4. 生成优化命令和预期收益
    5. 支持批量优化（可选）
    """
    
    # 图片目录
    WP_UPLOADS = "wp-content/uploads"
    
    # 支持的格式
    IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    
    def __init__(self, web_root: str, site_url: str, php_bin: str = "/www/server/php/82/bin/php"):
        self.web_root = web_root
        self.site_url = site_url.rstrip("/")
        self.php_bin = php_bin
        self.wp_uploads = os.path.join(web_root, self.WP_UPLOADS)
        self.wp_cli = "/usr/local/bin/wp"
    
    def _wp(self, args: str) -> Tuple[str, str, int]:
        cmd = f"cd {self.web_root} && WP_CLI_PHP={self.php_bin} {self.wp_cli} --allow-root {args}"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    
    def scan_images(self, max_depth: int = 3) -> List[ImageInfo]:
        """扫描上传目录中的所有图片"""
        images = []
        
        if not os.path.exists(self.wp_uploads):
            return images
        
        for root, dirs, files in os.walk(self.wp_uploads):
            # 限制深度
            depth = root.replace(self.wp_uploads, "").count(os.sep)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in self.IMAGE_FORMATS:
                    continue
                
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, self.web_root)
                url = f"{self.site_url}/{rel_path.replace(os.sep, '/')}"
                
                info = self.analyze_image(filepath, url)
                images.append(info)
        
        return images
    
    def analyze_image(self, filepath: str, url: str) -> ImageInfo:
        """分析单张图片"""
        info = ImageInfo(path=filepath, url=url)
        
        if not os.path.exists(filepath):
            info.issues.append("文件不存在")
            return info
        
        # 文件大小
        info.size_bytes = os.path.getsize(filepath)
        info.size_kb = info.size_bytes / 1024
        
        # 格式
        ext = os.path.splitext(filepath)[1].lower()
        info.format = ext.replace(".", "")
        
        # 图片尺寸
        try:
            result = subprocess.run(
                ["identify", "-format", "%w|%h", filepath],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and "|" in result.stdout:
                w, h = result.stdout.strip().split("|")
                info.width = int(w)
                info.height = int(h)
        except:
            # 尝试用 PHP GD
            pass
        
        # 分析问题和建议
        self._analyze_issues(info)
        
        return info
    
    def _analyze_issues(self, info: ImageInfo):
        """分析图片问题"""
        
        # 1. 未压缩（JPG）
        if info.format in ("jpg", "jpeg"):
            if info.size_kb > 200:
                info.compression_potential = 0.6
                info.issues.append(f"JPG过大({info.size_kb:.0f}KB)，可压缩60%+")
            elif info.size_kb > 100:
                info.compression_potential = 0.3
                info.issues.append(f"JPG可优化({info.size_kb:.0f}KB)")
        
        # 2. 无WebP
        if info.format in ("jpg", "jpeg", "png"):
            webp_path = info.path + ".webp"
            if not os.path.exists(webp_path):
                info.needs_webp = True
                info.issues.append("缺少WebP版本（可减少30-70%体积）")
        
        # 3. 无响应式
        # 检查是否有 srcset
        info.needs_responsive = True  # 需要检查HTML，这里简化
        
        # 4. 未压缩PNG
        if info.format == "png" and info.size_kb > 100:
            info.compression_potential = 0.7
            info.issues.append(f"PNG过大({info.size_kb:.0f}KB)，可压缩70%+")
        
        # 5. 估算节省空间
        if info.compression_potential > 0:
            info.estimated_size_kb = info.size_kb * (1 - info.compression_potential)
            info.savings_kb = info.size_kb - info.estimated_size_kb
        
        # 6. WebP节省
        if info.needs_webp:
            # WebP通常比JPG小30%
            webp_savings = info.size_kb * 0.3 if info.format in ("jpg", "jpeg") else info.size_kb * 0.5
            info.savings_kb += webp_savings
            info.estimated_size_kb = info.size_kb - webp_savings
    
    def generate_wp_cli_commands(self, images: List[ImageInfo]) -> List[Dict]:
        """生成 WP-CLI 优化命令"""
        commands = []
        
        for img in images:
            if not img.issues:
                continue
            
            cmd_info = {
                "path": img.path,
                "url": img.url,
                "current_size_kb": round(img.size_kb, 1),
                "estimated_size_kb": round(img.estimated_size_kb, 1),
                "savings_kb": round(img.savings_kb, 1),
                "issues": img.issues,
                "commands": []
            }
            
            # JPG压缩
            if "可压缩" in " ".join(img.issues):
                cmd_info["commands"].append({
                    "desc": f"压缩JPG ({img.size_kb:.0f}KB → {img.estimated_size_kb:.0f}KB)",
                    "cmd": f"jpegoptim --max=85 --size=200k {img.path}"
                })
            
            # PNG压缩
            if "PNG过大" in " ".join(img.issues):
                cmd_info["commands"].append({
                    "desc": f"压缩PNG ({img.size_kb:.0f}KB → {img.estimated_size_kb:.0f}KB)",
                    "cmd": f"optipng -o5 {img.path}"
                })
            
            # WebP生成
            if img.needs_webp:
                webp_path = img.path.rsplit(".", 1)[0] + ".webp"
                cmd_info["commands"].append({
                    "desc": f"生成WebP (节省~{img.size_kb*0.3:.0f}KB)",
                    "cmd": f"cwebp -q 80 {img.path} -o {webp_path}"
                })
            
            if cmd_info["commands"]:
                commands.append(cmd_info)
        
        return commands
    
    def run_full_analysis(self) -> ImageOptimizationReport:
        """运行完整图片分析"""
        print(f"🔍 开始扫描图片: {self.wp_uploads}")
        
        report = ImageOptimizationReport(site_url=self.site_url)
        
        images = self.scan_images()
        report.images = images
        report.total_images = len(images)
        
        total_bytes = sum(img.size_bytes for img in images)
        report.total_size_mb = total_bytes / (1024 * 1024)
        report.potential_savings_mb = sum(img.savings_kb for img in images) / 1024
        
        # 优化后大小（假设所有建议都执行）
        report.optimized_size_mb = report.total_size_mb - report.potential_savings_mb
        
        # 汇总问题
        issue_types = {"webp": 0, "compression": 0, "responsive": 0, "alt": 0}
        for img in images:
            if img.needs_webp:
                issue_types["webp"] += 1
            if img.compression_potential > 0.2:
                issue_types["compression"] += 1
        
        if issue_types["webp"] > 0:
            report.recommendations.append(
                f"📦 为 {issue_types['webp']} 张图片生成WebP版本（节省{report.potential_savings_mb:.1f}MB）"
            )
        if issue_types["compression"] > 0:
            report.recommendations.append(
                f"🗜️ 压缩 {issue_types['compression']} 张未优化图片"
            )
        
        print(f"\n✅ 扫描完成!")
        print(f"   图片总数: {report.total_images}")
        print(f"   总体积: {report.total_size_mb:.2f}MB")
        print(f"   可节省: {report.potential_savings_mb:.2f}MB")
        print(f"   优化后: {report.optimized_size_mb:.2f}MB")
        
        return report
    
    def export_commands(self, images: List[ImageInfo]) -> str:
        """导出优化命令脚本"""
        cmds = self.generate_wp_cli_commands(images)
        
        output = "#!/bin/bash\n"
        output += "# Auto-Claw 图片优化命令\n"
        output += f"# 站点: {self.site_url}\n"
        output += "# 执行前请备份!\n\n"
        
        for item in cmds:
            output += f"# {item['url']} ({item['current_size_kb']}KB)\n"
            for cmd in item["commands"]:
                output += f"# 节省 ~{item['savings_kb']}KB\n"
                output += f"{cmd['cmd']}\n"
            output += "\n"
        
        return output
