#!/usr/bin/env python3
"""
AI工具箱 - 简洁优雅 全覆盖 主流AI工具
"""
import json, subprocess, webbrowser, os
from typing import List, Dict, Optional

# ==================== 工具数据库 (精简主流) ====================
TOOLS = {
    # AI写作
    "写作": [
        {"name":"笔灵AI写作","url":"https://ibiling.cn","desc":"论文、公文"},
        {"name":"新华妙笔","url":"https://mx.bi118.cn","desc":"公文写作"},
        {"name":"蛙蛙写作","url":"https://www.wawawrite.com","desc":"小说创作"},
        {"name":"讯飞绘文","url":"https://turbotype.xfyun.cn","desc":"智能写作"},
        {"name":"稿定AI文案","url":"https://www.gaoding.com","desc":"文案生成"},
        {"name":"千笔AI论文","url":"https://www.qianbi.cc","desc":"论文写作"},
        {"name":"66AI论文","url":"https://www.66paper.com","desc":"论文助手"},
        {"name":"万知","url":"https://www.wanzhi.com","desc":"AI问答阅读"},
        {"name":"包阅AI","url":"https://baoyueai.com","desc":"阅读助手"},
    ],
    # AI图像
    "图像": [
        {"name":"Midjourney","url":"https://www.midjourney.com","desc":"AI绘图"},
        {"name":"Stable Diffusion","url":"https://stability.ai","desc":"开源绘图"},
        {"name":"LiblibAI","url":"https://www.liblib.ai","desc":"中文绘图"},
        {"name":"通义万相","url":"https://tongyi.aliyun.com","desc":"阿里绘图"},
        {"name":"可灵AI","url":"https://klingai.kuaishou.com","desc":"快手视频"},
        {"name":"秒画","url":"https://miaohua.sensetime.com","desc":"商汤绘图"},
        {"name":"WHEE","url":"https://www.whee.com","desc":"美图AI"},
        {"name":"美图设计室","url":"https://www.desk.xiaomihong.com","desc":"设计工具"},
        {"name":"堆友AI","url":"https://d.designai.aliyun.com","desc":"阿里堆友"},
        {"name":"绘蛙","url":"https://www.ihuao.com","desc":"电商绘图"},
        {"name":"Civitai","url":"https://civitai.com","desc":"模型分享"},
        {"name":"哩布哩布","url":"https://liblib.com","desc":"中文模型"},
        {"name":"360智图","url":"https://360tupian.com","desc":"AI修图"},
    ],
    # AI视频
    "视频": [
        {"name":"即梦AI","url":"https://jimeng.jianying.com","desc":"字节视频"},
        {"name":"可灵AI视频","url":"https://klingai.kuaishou.com/video","desc":"视频生成"},
        {"name":"Runway","url":"https://runwayml.com","desc":"视频编辑"},
        {"name":"Sora","url":"https://openai.com/sora","desc":"OpenAI视频"},
        {"name":"HeyGen","url":"https://www.heygen.com","desc":"数字人"},
        {"name":"有言","url":"https://www.youyanai.com","desc":"3D虚拟人"},
        {"name":"白日梦","url":"https://www.baichengai.com","desc":"AI视频"},
        {"name":"Vidu","url":"https://www.vidu.studio","desc":"生数科技"},
        {"name":"腾讯混元","url":"https://hunyuan.tencent.com","desc":"腾讯视频"},
        {"name":"讯飞绘镜","url":"https://huijing.xfyun.cn","desc":"讯飞AI视频"},
        {"name":"智谱清影","url":"https://www.zhipuai.cn","desc":"AI视频"},
    ],
    # AI编程
    "编程": [
        {"name":"Cursor","url":"https://cursor.sh","desc":"AI IDE"},
        {"name":"Claude Code","url":"https://claude.com/code","desc":"编程助手"},
        {"name":"GitHub Copilot","url":"https://github.com/features/copilot","desc":"代码补全"},
        {"name":"Trae","url":"https://www.trae.ai","desc":"字节IDE"},
        {"name":"Windsurf","url":"https://windsurf.com","desc":"AI编辑器"},
        {"name":"Bolt.new","url":"https://bolt.new","desc":"全栈开发"},
        {"name":"Replit Agent","url":"https://replit.com/agent","desc":"AI编程"},
        {"name":"通义灵码","url":"https://tongyi.aliyun.com/lingma","desc":"阿里编程"},
        {"name":"CodeRabbit","url":"https://coderabbit.ai","desc":"代码审查"},
        {"name":"v0","url":"https://v0.dev","desc":"UI生成"},
        {"name":"Firebase Studio","url":"https://firebase.google.com/studio","desc":"谷歌开发"},
    ],
    # AI办公
    "办公": [
        {"name":"AiPPT","url":"https://www.aippt.cn","desc":"PPT生成"},
        {"name":"Gamma","url":"https://gamma.app","desc":"PPT生成"},
        {"name":"Kimi PPT","url":"https://kimi.moonshot.cn","desc":"PPT助手"},
        {"name":"讯飞智文","url":"https://zhiwen.xfyun.cn","desc":"文档生成"},
        {"name":"iSlide","url":"https://www.islide.cc","desc":"PPT插件"},
        {"name":"飞象AI","url":"https://www.ifeixiang.com","desc":"表格处理"},
        {"name":"WPS AI","url":"https://ai.wps.cn","desc":"WPS助手"},
        {"name":"百度文库","url":"https://wenku.baidu.com","desc":"文档AI"},
        {"name":"ProcessOn","url":"https://www.processon.com","desc":"思维导图"},
        {"name":"亿图脑图","url":"https://www.edrawmax.cn","desc":"思维导图"},
        {"name":"博思白板","url":"https://www.bosboard.com","desc":"在线白板"},
    ],
    # AI搜索
    "搜索": [
        {"name":"秘塔AI搜索","url":"https://metaso.cn","desc":"无广告搜索"},
        {"name":"Perplexity","url":"https://www.perplexity.ai","desc":"AI搜索引擎"},
        {"name":"夸克AI","url":"https://www.quark.cn","desc":"阿里搜索"},
        {"name":"天工AI搜索","url":"https://www.tiangong.cn","desc":"昆仑万维"},
        {"name":"Felo","url":"https://felo.ai","desc":"多语言搜索"},
        {"name":"360AI搜索","url":"https://ai.360.com","desc":"360搜索"},
        {"name":"知乎直答","url":"https://www.zhihu.com/topic","desc":"知乎搜索"},
        {"name":"心流","url":"https://www.ifoof.com","desc":"AI搜索"},
    ],
    # AI聊天
    "聊天": [
        {"name":"ChatGPT","url":"https://chat.openai.com","desc":"OpenAI"},
        {"name":"Claude","url":"https://claude.ai","desc":"Anthropic"},
        {"name":"DeepSeek","url":"https://chat.deepseek.com","desc":"深度求索"},
        {"name":"Kimi","url":"https://kimi.moonshot.cn","desc":"月之暗面"},
        {"name":"豆包","url":"https://www.doubao.com","desc":"字节跳动"},
        {"name":"文心一言","url":"https://yiyan.baidu.com","desc":"百度"},
        {"name":"通义千问","url":"https://tongyi.aliyun.com","desc":"阿里"},
        {"name":"智谱清言","url":"https://www.zhipuai.cn","desc":"智谱AI"},
        {"name":"讯飞星火","url":"https://xinghuo.xfyun.cn","desc":"讯飞"},
        {"name":"腾讯元宝","url":"https://yuanbao.tencent.com","desc":"腾讯"},
    ],
    # AI音频
    "音频": [
        {"name":"Suno","url":"https://suno.ai","desc":"AI音乐"},
        {"name":"ElevenLabs","url":"https://elevenlabs.io","desc":"TTS"},
        {"name":"讯飞智作","url":"https://zhoz.xfyun.cn","desc":"配音合成"},
        {"name":"海螺AI","url":"https://minimax.chat","desc":"MiniMax"},
        {"name":"网易天音","url":"https://tianyin.163.com","desc":"音乐生成"},
        {"name":"琅琅配音","url":"https://www.longlang.ai","desc":"TTS"},
        {"name":"Udio","url":"https://www.udio.com","desc":"AI音乐"},
        {"name":"Stable Audio","url":"https://stableaudio.com","desc":"音频生成"},
    ],
    # AI设计
    "设计": [
        {"name":"Figma AI","url":"https://www.figma.com","desc":"UI设计"},
        {"name":"Canva","url":"https://www.canva.com","desc":"在线设计"},
        {"name":"美图AI","url":"https://design.xiaomihong.com","desc":"设计工具"},
        {"name":"稿定设计","url":"https://www.gaoding.com","desc":"设计平台"},
        {"name":"创客贴","url":"https://www.chuangkit.com","desc":"在线设计"},
        {"name":"MasterGo","url":"https://mastergo.com","desc":"协作设计"},
        {"name":"Pixso AI","url":"https://pixso.cn","desc":"UI设计"},
        {"name":"Framer","url":"https://www.framer.com","desc":"网站设计"},
    ],
    # AI智能体
    "智能体": [
        {"name":"扣子Coze","url":"https://www.coze.com","desc":"字节Agent"},
        {"name":"Manus","url":"https://manus.im","desc":"通用Agent"},
        {"name":"OpenClaw","url":"https://openclaws.io","desc":"开源助手"},
        {"name":"Dify","url":"https://dify.ai","desc":"LLM应用"},
        {"name":"FastGPT","url":"https://fastgpt.cn","desc":"知识库"},
        {"name":"文心智能体","url":"https://agents.baidu.com","desc":"百度Agent"},
        {"name":"讯飞星辰","url":"https://xingchen.xfyun.cn","desc":"讯飞Agent"},
        {"name":"阿里Agent","url":"https://www.aliyundrive.com","desc":"阿里Agent"},
    ],
    # AI翻译
    "翻译": [
        {"name":"DeepL","url":"https://www.deepl.com","desc":"精准翻译"},
        {"name":"Google翻译","url":"https://translate.google.com","desc":"谷歌翻译"},
        {"name":"腾讯翻译","url":"https://fanyi.qq.com","desc":"腾讯翻译"},
        {"name":"讯飞翻译","url":"https://fanyi.xfyun.cn","desc":"讯飞翻译"},
        {"name":"火山翻译","url":"https://translate.volcengine.com","desc":"字节翻译"},
        {"name":"百度翻译","url":"https://fanyi.baidu.com","desc":"百度翻译"},
    ],
    # AI开发平台
    "开发平台": [
        {"name":"阿里云百炼","url":"https://bailian.aliyun.com","desc":"阿里MaaS"},
        {"name":"百度智能云","url":"https://cloud.baidu.com","desc":"百度AI"},
        {"name":"腾讯云AI","url":"https://cloud.tencent.com","desc":"腾讯AI"},
        {"name":"讯飞开放平台","url":"https://www.xfyun.cn","desc":"讯飞AI"},
        {"name":"Google AI","url":"https://ai.google","desc":"谷歌AI"},
        {"name":"Azure AI","url":"https://azure.microsoft.com/ai","desc":"微软AI"},
        {"name":"AWS AI","url":"https://aws.amazon.com/ai","desc":"亚马逊AI"},
        {"name":"魔搭社区","url":"https://www.modelscope.cn","desc":"阿里模型"},
        {"name":"HuggingFace","url":"https://huggingface.co","desc":"模型中心"},
    ],
    # AI学习
    "学习": [
        {"name":"Coursera","url":"https://www.coursera.org","desc":"在线课程"},
        {"name":"fast.ai","url":"https://www.fast.ai","desc":"深度学习"},
        {"name":"DeepLearning.AI","url":"https://www.deeplearning.ai","desc":"AI课程"},
        {"name":"Kaggle","url":"https://www.kaggle.com","desc":"数据科学"},
        {"name":"飞桨AI Studio","url":"https://aistudio.baidu.com","desc":"百度AI学习"},
        {"name":"AI大学堂","url":"https://aiuap.baidu.com","desc":"百度AI"},
    ],
    # AI检测
    "检测": [
        {"name":"GPTZero","url":"https://gptzero.me","desc":"AI检测"},
        {"name":"朱雀AI检测","url":"https://www.zhuqueai.com","desc":"内容检测"},
        {"name":"笔灵AI降重","url":"https://ibiling.cn","desc":"降AI率"},
        {"name":"知网AIGC","url":"https://cx.cnki.net","desc":"学术检测"},
        {"name":"维普AI检测","url":"https://ai.cqvip.com","desc":"论文检测"},
    ],
}

# ==================== 功能函数 ====================
def find(keyword: str, cat: str = None) -> List[Dict]:
    results = []
    kw = keyword.lower()
    for c, tools in TOOLS.items():
        if cat and c != cat: continue
        for t in tools:
            if kw in t["name"].lower() or kw in t.get("desc","").lower():
                results.append(t)
    return results[:10]

def category(cat: str) -> List[Dict]:
    return TOOLS.get(cat, [])

def tool(name: str) -> Optional[Dict]:
    n = name.lower()
    for tools in TOOLS.values():
        for t in tools:
            if n in t["name"].lower():
                return t
    return None

def call(name: str, **kwargs) -> Dict:
    t = tool(name)
    if t:
        return {"status":"ok","tool":t["name"],"url":t["url"]}
    return {"status":"error","message":f"未找到: {name}"}

def list_cats() -> List[str]:
    return list(TOOLS.keys())

def stats() -> Dict:
    return {c: len(t) for c, t in TOOLS.items()}

__all__ = ["find","category","tool","call","list_cats","stats","TOOLS"]
