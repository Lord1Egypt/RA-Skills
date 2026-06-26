#!/usr/bin/env python3
"""
古风小生模式 - 无典故压缩器
核心目标：在保持技术准确性的前提下，最大化减少token使用量
完全无典故，只用极简文言
"""

import re
from typing import Dict, List, Optional, Tuple


class ClassicalCompressorNoAllusion:
    """古风压缩器 - 无典故版本，专注于减少token"""
    
    def __init__(self):
        # 极简文言词汇映射（一个字代替多个字）
        self.classical_map = {
            # 技术术语压缩 - 核心部分
            "数据库": "库",
            "服务器": "服", 
            "网络": "网",
            "配置": "配",
            "错误": "错",
            "问题": "问",
            "解决方案": "解",
            "性能": "性",
            "内存": "存",
            "缓存": "缓",
            "日志": "志",
            "代码": "码",
            "函数": "函",
            "变量": "变",
            "数组": "组",
            "对象": "对",
            "接口": "口",
            "协议": "议",
            "请求": "请",
            "响应": "应",
            "数据": "数",
            "文件": "件",
            "系统": "系",
            "程序": "程",
            "应用": "用",
            "软件": "软",
            "硬件": "硬",
            "设备": "设",
            "资源": "资",
            "权限": "权",
            "用户": "户",
            
            # 操作动词压缩
            "检查": "检",
            "测试": "测", 
            "验证": "验",
            "修复": "修",
            "优化": "优",
            "部署": "部",
            "启动": "启",
            "停止": "停",
            "连接": "连",
            "断开": "断",
            "上传": "上",
            "下载": "下",
            "安装": "安",
            "卸载": "卸",
            "创建": "建",
            "删除": "删",
            "修改": "改",
            "复制": "复",
            "移动": "移",
            "搜索": "搜",
            "排序": "排",
            "过滤": "滤",
            "加密": "密",
            "解密": "解",
            
            # 文言虚词
            "的": "",  # 直接省略
            "地": "",  # 直接省略  
            "得": "",  # 直接省略
            "了": "",  # 直接省略
            "着": "",  # 直接省略
            "过": "",  # 直接省略
            "因为": "盖",
            "所以": "故",
            "如果": "若",
            "那么": "则",
            "应该": "宜",
            "可以": "可",
            "必须": "须",
            "但是": "然",
            "而且": "且",
            "或者": "或",
            "并且": "并",
            "然后": "后",
            "之后": "后",
            "之前": "前",
            "之后": "后",
            "之中": "中",
            "之内": "内",
            "之外": "外",
            "之上": "上",
            "之下": "下",
            
            # 连接词压缩
            "导致": "→",
            "引起": "→",
            "造成": "→",
            "因此": "→",
            "于是": "→",
        }
        
        # 需要完整保留的关键词（不压缩）
        self.preserve_keywords = [
            "API", "HTTP", "HTTPS", "JSON", "XML", "SQL", "NoSQL",
            "React", "Vue", "Angular", "Node.js", "Python", "Java",
            "JavaScript", "TypeScript", "Docker", "Kubernetes", "Git",
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "Nginx", "Apache",
            "Windows", "Linux", "macOS", "iOS", "Android", "Chrome",
            "Firefox", "Safari", "Edge", "useMemo", "useEffect", "useState",
            "useCallback", "useRef", "useContext", "useReducer",
        ]
    
    def compress_text(self, text: str) -> str:
        """
        压缩文本，最大化减少token，完全无典故
        
        Args:
            text: 原始文本
            
        Returns:
            str: 压缩后的古风文本（无典故）
        """
        if not text:
            return ""
        
        # 1. 统一小写（保留关键术语）
        compressed = text
        
        # 2. 保护关键词（不压缩）
        for keyword in self.preserve_keywords:
            placeholder = f"__{keyword.upper()}__"
            compressed = compressed.replace(keyword, placeholder)
            compressed = compressed.replace(keyword.lower(), placeholder)
        
        # 3. 应用文言映射（长词优先）
        # 按长度降序排序，先匹配长词
        sorted_items = sorted(self.classical_map.items(), key=lambda x: len(x[0]), reverse=True)
        for original, replacement in sorted_items:
            if original in compressed:
                compressed = compressed.replace(original, replacement)
        
        # 4. 恢复关键词
        for keyword in self.preserve_keywords:
            placeholder = f"__{keyword.upper()}__"
            compressed = compressed.replace(placeholder, keyword)
        
        # 5. 删除多余空格和标点
        compressed = re.sub(r'\s+', ' ', compressed)  # 多个空格变一个
        compressed = re.sub(r'([，。；！？])\s+', r'\1', compressed)  # 删除标点后空格
        compressed = compressed.strip()
        
        # 6. 应用古风格式优化
        compressed = self._apply_classical_format(compressed)
        
        return compressed
    
    def _apply_classical_format(self, text: str) -> str:
        """应用古风格式优化"""
        result = text
        
        # 删除多余的"的"、"了"等虚词（可能还有残留）
        result = re.sub(r'[的地得着了过]', '', result)
        
        # 用→替换一些连接词
        result = re.sub(r'(因为|由于|所以|因此|于是|导致|引起|造成)', '→', result)
        
        # 简化句子结构
        result = re.sub(r'请', '', result)  # 删除客套话
        result = re.sub(r'可以尝试', '可试', result)
        result = re.sub(r'建议您', '建议', result)
        result = re.sub(r'可能需要', '或需', result)
        
        # 删除句尾语气词
        result = re.sub(r'[吧呢啊呀啦]', '', result)
        
        return result
    
    def analyze_compression(self, original: str, compressed: str) -> Dict:
        """分析压缩效果"""
        orig_len = len(original)
        comp_len = len(compressed)
        reduction = (orig_len - comp_len) / orig_len * 100 if orig_len > 0 else 0
        
        return {
            "original_length": orig_len,
            "compressed_length": comp_len,
            "reduction_percent": round(reduction, 1),
            "reduction_chars": orig_len - comp_len,
            "compression_ratio": round(comp_len / orig_len * 100, 1) if orig_len > 0 else 0
        }
    
    def test_compression(self):
        """测试压缩效果"""
        test_cases = [
            # 普通现代文本
            "数据库连接失败，请检查网络配置和服务器状态。",
            "React组件一直在重新渲染，可能是因为在组件内部创建了新的对象或函数。",
            "需要优化系统性能，建议增加缓存和减少数据库查询次数。",
            "文件上传失败，可能是网络问题或者服务器磁盘空间不足。",
            "API请求超时，需要检查网络连接和服务器负载。",
        ]
        
        print("=" * 60)
        print("古风小生模式 - 无典故压缩测试")
        print("=" * 60)
        
        total_original = 0
        total_compressed = 0
        
        for i, test in enumerate(test_cases, 1):
            compressed = self.compress_text(test)
            analysis = self.analyze_compression(test, compressed)
            
            print(f"\n测试 {i}:")
            print(f"原始: {test}")
            print(f"古风: {compressed}")
            print(f"统计: {analysis['original_length']}字 → {analysis['compressed_length']}字")
            print(f"节省: {analysis['reduction_percent']}% ({analysis['reduction_chars']}字)")
            
            total_original += analysis['original_length']
            total_compressed += analysis['compressed_length']
        
        # 总体统计
        total_reduction = (total_original - total_compressed) / total_original * 100
        print(f"\n" + "=" * 60)
        print(f"总体统计:")
        print(f"总原始长度: {total_original}字")
        print(f"总压缩长度: {total_compressed}字")
        print(f"总体节省: {round(total_reduction, 1)}% ({total_original - total_compressed}字)")
        print("=" * 60)
        
        return {
            "total_original": total_original,
            "total_compressed": total_compressed,
            "total_reduction": round(total_reduction, 1)
        }


if __name__ == "__main__":
    compressor = ClassicalCompressorNoAllusion()
    results = compressor.test_compression()
    
    print("\n[OK] 古风小生模式 - 无典故版本")
    print("特点:")
    print("1. 完全无典故，只用最直接的技术表述")
    print("2. 单字词优先，最大化减少token")
    print("3. 删除所有虚词和冗余连接词")
    print("4. 用→符号代替文字连接")
    print(f"\n平均节省: {results['total_reduction']}% token")