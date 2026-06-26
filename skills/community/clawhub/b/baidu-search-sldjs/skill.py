import webbrowser
import urllib.parse
from core.skill import BaseSkill  # 必须导入框架基类

class BaiduSearchSldjsSkill(BaseSkill):
    # 技能唯一标识（不能重复）
    name = "baidu-search-sldjs"
    # 触发关键词，用户输入这些词时会触发该技能
    triggers = ["百度搜索", "搜百度", "打开百度搜索"]
    
    def execute(self, query, **kwargs):
        """
        OpenClaw 技能的核心执行方法
        Args:
            query (str): 用户的原始提问
            **kwargs: 框架传递的其他参数
        Returns:
            str: 技能执行结果
        """
        # 从用户提问中提取搜索关键词（这里简化处理，直接用整个query）
        keyword = query
        
        # 对关键字进行URL编码
        encoded_keyword = urllib.parse.quote(keyword)
        # 构建百度搜索URL
        baidu_search_url = f"https://www.baidu.com/s?wd={encoded_keyword}"
        # 打开默认浏览器
        webbrowser.open(baidu_search_url)
        
        return f"✅ 已在浏览器中打开：{keyword}"