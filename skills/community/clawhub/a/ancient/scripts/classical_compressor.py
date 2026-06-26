#!/usr/bin/env python3
"""
古风小生模式 - 无典故压缩器（主版本）
核心目标：在保持技术准确性的前提下，最大化减少token使用量
完全无典故，只用极简文言
"""

import re
from typing import Dict, List, Optional, Tuple


class ClassicalCompressor:
    """古风压缩器 - 无典故版本，专注于减少token"""
    
    def __init__(self):
        # 极致文言词汇映射（最高压缩率）
        self.classical_map = {
            # 技术术语极致压缩
            "数据库": "库", "服务器": "服", "网络": "网", "配置": "配",
            "错误": "错", "问题": "问", "解决方案": "解", "性能": "性",
            "内存": "存", "缓存": "缓", "日志": "志", "代码": "码",
            "函数": "函", "变量": "变", "数组": "组", "对象": "对",
            "接口": "口", "协议": "议", "请求": "请", "响应": "应",
            "数据": "数", "文件": "件", "系统": "系", "程序": "程",
            "应用": "用", "软件": "软", "硬件": "硬", "设备": "设",
            "资源": "资", "权限": "权", "用户": "户", "连接": "连",
            "状态": "态", "时间": "时", "空间": "空", "速度": "速",
            "容量": "量", "频率": "频", "温度": "温", "压力": "压",
            "质量": "质", "安全": "安", "可靠": "靠", "稳定": "稳",
            
            # 操作动词极致压缩
            "检查": "检", "测试": "测", "验证": "验", "修复": "修",
            "优化": "优", "部署": "部", "启动": "启", "停止": "停",
            "断开": "断", "上传": "上", "下载": "下", "安装": "安",
            "卸载": "卸", "创建": "建", "删除": "删", "修改": "改",
            "复制": "复", "移动": "移", "搜索": "搜", "排序": "排",
            "过滤": "滤", "加密": "密", "解密": "解", "分析": "析",
            "设计": "设", "开发": "开", "测试": "测", "发布": "发",
            "更新": "更", "备份": "备", "恢复": "恢", "监控": "监",
            "报警": "警", "统计": "统", "计算": "算", "处理": "处",
            "存储": "储", "传输": "输", "接收": "收", "发送": "发",
            "打印": "印", "扫描": "扫", "读取": "读", "写入": "写",
            "编译": "编", "解释": "释", "调试": "调", "跟踪": "踪",
            "记录": "记", "保存": "存", "加载": "载", "导出": "出",
            "导入": "入", "转换": "转", "合并": "合", "拆分": "拆",
            
            # 极致虚词删除
            "的": "", "地": "", "得": "", "了": "", "着": "", "过": "",
            "在": "", "和": "", "或": "", "与": "", "及": "", "以及": "",
            "并且": "", "或者": "", "还是": "", "但是": "然", "然而": "然",
            "不过": "然", "可是": "然", "因为": "盖", "由于": "盖",
            "所以": "故", "因此": "故", "于是": "故", "如果": "若",
            "假如": "若", "要是": "若", "那么": "则", "然后": "后",
            "之后": "后", "之前": "前", "之中": "中", "之内": "内",
            "之外": "外", "之上": "上", "之下": "下", "可能": "或",
            "也许": "或", "大概": "或", "应该": "宜", "应当": "宜",
            "必须": "须", "需要": "需", "可以": "可", "能够": "能",
            
            # 连接词用符号代替
            "导致": "→", "引起": "→", "造成": "→", "使得": "→",
            "致使": "→", "结果": "→", "最终": "→", "于是": "→",
            "因此": "→", "所以": "→", "因为": "→", "由于": "→",
            
            # 客套话完全删除
            "请": "", "麻烦": "", "您好": "", "你好": "", "谢谢": "",
            "感谢": "", "抱歉": "", "对不起": "", "不好意思": "",
            "请问": "", "请教": "", "帮忙": "", "帮助": "", "协助": "",
            "支持": "", "好的": "", "明白了": "", "没问题": "",
        }
        
        # 需要完整保留的关键词（不压缩）
        self.preserve_keywords = [
            "API", "HTTP", "HTTPS", "JSON", "XML", "SQL", "NoSQL",
            "React", "Vue", "Angular", "Node", "Python", "Java",
            "JavaScript", "TypeScript", "Docker", "Kubernetes", "Git",
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "Nginx", "Apache",
            "Windows", "Linux", "macOS", "iOS", "Android", "Chrome",
            "Firefox", "Safari", "Edge",
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
        
        # 1. 保护关键词
        compressed = text
        for keyword in self.preserve_keywords:
            placeholder = f"__{keyword.upper()}__"
            compressed = compressed.replace(keyword, placeholder)
            compressed = compressed.replace(keyword.lower(), placeholder)
        
        # 2. 应用极致文言映射（长词优先）
        sorted_items = sorted(self.classical_map.items(), key=lambda x: len(x[0]), reverse=True)
        for original, replacement in sorted_items:
            compressed = compressed.replace(original, replacement)
        
        # 3. 恢复关键词
        for keyword in self.preserve_keywords:
            placeholder = f"__{keyword.upper()}__"
            compressed = compressed.replace(placeholder, keyword)
        
        # 4. 极致优化
        compressed = self._apply_ultimate_optimization(compressed)
        
        return compressed
    
    def _apply_ultimate_optimization(self, text: str) -> str:
        """应用极致优化"""
        result = text
        
        # 删除所有标点（保留→）
        result = re.sub(r'[，。；！？、：；"\'（）《》【】]', ' ', result)
        
        # 删除所有虚词（二次清理）
        result = re.sub(r'[的地得着了过着在是和或与及]', '', result)
        
        # 用→替换连接词
        result = re.sub(r'(因为|由于|所以|因此|于是|导致|引起|造成|使得|致使|结果|最终)', '→', result)
        
        # 删除多余空格
        result = re.sub(r'\s+', ' ', result)
        
        # 极致句子结构
        result = re.sub(r'可以尝试', '试', result)
        result = re.sub(r'建议您', '建议', result)
        result = re.sub(r'可能需要', '需', result)
        result = re.sub(r'应该考虑', '考虑', result)
        result = re.sub(r'必须确保', '确保', result)
        
        # 删除句尾语气词
        result = re.sub(r'[吧呢啊呀啦嘛哇哦哟]', '', result)
        
        # 用符号替换常见结构
        result = re.sub(r'检查一下', '检', result)
        result = re.sub(r'测试一下', '测', result)
        result = re.sub(r'验证一下', '验', result)
        result = re.sub(r'修复一下', '修', result)
        
        return result.strip()
    
    def analyze_compression(self, original: str, compressed: str) -> Dict:
        """分析压缩效果"""
        orig_len = len(original.replace(' ', ''))
        comp_len = len(compressed.replace(' ', ''))
        reduction = (orig_len - comp_len) / orig_len * 100 if orig_len > 0 else 0
        
        return {
            "original_length": len(original),
            "original_chars": orig_len,
            "compressed_length": len(compressed),
            "compressed_chars": comp_len,
            "reduction_percent": round(reduction, 1),
            "reduction_chars": orig_len - comp_len,
        }
    
    def test_compression(self):
        """测试压缩效果"""
        test_cases = [
            "数据库连接失败，请检查网络配置和服务器状态。",
            "React组件一直在重新渲染，可能是因为在组件内部创建了新的对象或函数。",
            "需要优化系统性能，建议增加缓存和减少数据库查询次数。",
            "文件上传失败，可能是网络问题或者服务器磁盘空间不足。",
            "API请求超时，需要检查网络连接和服务器负载。",
            "您好，请问如何解决数据库连接超时的问题？",
        ]
        
        print("=" * 60)
        print("古风小生模式 - 无典故压缩测试")
        print("=" * 60)
        
        total_original_chars = 0
        total_compressed_chars = 0
        
        for i, test in enumerate(test_cases, 1):
            compressed = self.compress_text(test)
            analysis = self.analyze_compression(test, compressed)
            
            print(f"\n测试 {i}:")
            print(f"原始: {test}")
            print(f"古风: {compressed}")
            print(f"统计: {analysis['original_chars']}字符 → {analysis['compressed_chars']}字符")
            print(f"节省: {analysis['reduction_percent']}% ({analysis['reduction_chars']}字符)")
            
            total_original_chars += analysis['original_chars']
            total_compressed_chars += analysis['compressed_chars']
        
        # 总体统计
        total_reduction = (total_original_chars - total_compressed_chars) / total_original_chars * 100
        print(f"\n" + "=" * 60)
        print(f"总体统计:")
        print(f"总原始字符: {total_original_chars}字符")
        print(f"总压缩字符: {total_compressed_chars}字符")
        print(f"总体节省: {round(total_reduction, 1)}% ({total_original_chars - total_compressed_chars}字符)")
        print("=" * 60)
        
        return {
            "total_original_chars": total_original_chars,
            "total_compressed_chars": total_compressed_chars,
            "total_reduction": round(total_reduction, 1)
        }


if __name__ == "__main__":
    compressor = ClassicalCompressor()
    results = compressor.test_compression()
    
    print("\n[无典故版] 古风小生模式")
    print("核心特点:")
    print("1. 完全无典故，只用最直接的技术表述")
    print("2. 极致单字词，追求最高压缩率")
    print("3. 删除所有虚词、客套话、冗余词")
    print("4. 用→符号代替文字连接")
    print(f"\n字符节省: {results['total_reduction']}%")
    print(f"平均每100字节省约{int(results['total_reduction'])}字")