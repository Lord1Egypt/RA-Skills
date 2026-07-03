from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_baidu_trending(
    args: null
) -> Dict[str, Any]:
    """
    获取百度热榜，包含实时热搜、社会热点、科技新闻、娱乐八卦等多领域的热门中文资讯和搜索趋势
    
    Args:
        args: null
    
    Returns:
        null
    """
    arguments = {
        "args": args
    }
    
    return call_api("1777419061629955", "get_baidu_trending", arguments)

def get_36kr_trending(
    type: Optional[str] = "hot"
) -> Dict[str, Any]:
    """
    获取 36 氪热榜，提供创业、商业、科技领域的热门资讯，包含投融资动态、新兴产业分析和商业模式创新信息
    
    Args:
        type: 分类: hot(人气榜), video(视频榜), comment(热议榜), collect(收藏榜)
    
    Returns:
        null
    """
    arguments = {
        "type": type
    }
    
    return call_api("1777419061629955", "get_36kr_trending", arguments)

def get_autohome_trending(
    args: null
) -> Dict[str, Any]:
    """
    获取汽车之家热榜，包含汽车新闻、新车发布、购车指南、试驾体验、汽车评测及汽车行业动态的专业汽车资讯
    
    Args:
        args: null
    
    Returns:
        null
    """
    arguments = {
        "args": args
    }
    
    return call_api("1777419061629955", "get_autohome_trending", arguments)

def get_bbc_news(
    category: Optional[str] = "",
    edition: Optional[str] = ""
) -> Dict[str, Any]:
    """
    获取 BBC 新闻，提供全球新闻、英国新闻、商业、政治、健康、教育、科技、娱乐等资讯
    
    Args:
        category: 新闻分类：''(热门), world(国际), uk(英国), business(商业), politics(政治), health(健康), education(教育), science_and_environment(科学与环境), technology(科技), entertainment_and_arts(娱乐与艺术)
        edition: 版本：''(默认), uk(英国), us(美国和加拿大), int(世界其他地区)，仅对category为空时有效
    
    Returns:
        null
    """
    arguments = {
        "category": category,
        "edition": edition
    }
    
    return call_api("1777419061629955", "get_bbc_news", arguments)

def get_bilibili_rank(
    rank_type: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    获取哔哩哔哩视频排行榜，包含全站、动画、音乐、游戏等多个分区的热门视频，反映当下年轻人的内容消费趋势
    
    Args:
        rank_type: 排行榜分区：0(全站), 1(动画), 3(音乐), 4(游戏), 5(娱乐), 188(科技), 119(鬼畜), 129(舞蹈), 155(时尚), 160(生活), 168(国创相关), 181(影视)
    
    Returns:
        null
    """
    arguments = {
        "rank_type": rank_type
    }
    
    return call_api("1777419061629955", "get_bilibili_rank", arguments)

def get_bilibili_trending(
) -> Dict[str, Any]:
    """
    获取哔哩哔哩热门视频
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_bilibili_trending", arguments)

def get_douban_rank(
    rank_type: Optional[str] = "subject",
    start: Optional[int] = 0.0,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    获取豆瓣实时热门榜单，提供当前热门的图书、电影、电视剧、综艺等作品信息，包含评分和热度数据
    
    Args:
        rank_type: 榜单类型：subject(图书、电影、电视剧、综艺等), movie(电影), tv(电视剧)
        start: 起始位置
        count: 返回结果数量
    
    Returns:
        null
    """
    arguments = {
        "rank_type": rank_type,
        "start": start,
        "count": count
    }
    
    return call_api("1777419061629955", "get_douban_rank", arguments)

def get_infoq_news(
    region: Optional[str] = "cn"
) -> Dict[str, Any]:
    """
    获取 InfoQ 技术资讯，包含软件开发、架构设计、云计算、AI等企业级技术内容和前沿开发者动态
    
    Args:
        region: 地区选择：cn(中文版), global(国际版)
    
    Returns:
        null
    """
    arguments = {
        "region": region
    }
    
    return call_api("1777419061629955", "get_infoq_news", arguments)

def get_ithome_trending(
) -> Dict[str, Any]:
    """
    获取IT之家热榜，包含科技资讯、数码产品、互联网动态、软件应用及前沿科技发展的热门中文科技新闻
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_ithome_trending", arguments)

def get_netease_news_trending(
) -> Dict[str, Any]:
    """
    获取网易新闻热点榜，包含时政要闻、社会事件、财经资讯、科技动态及娱乐体育的全方位中文新闻资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_netease_news_trending", arguments)

def get_sogou_trending(
) -> Dict[str, Any]:
    """
    获取搜狗热搜榜，包含搜狗搜索平台的热门搜索关键词、实时搜索趋势及用户关注的热点中文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_sogou_trending", arguments)

def get_sspai_rank(
    tag: Optional[str] = "热门文章",
    limit: Optional[int] = 40.0
) -> Dict[str, Any]:
    """
    获取少数派热榜，包含数码产品评测、软件应用推荐、生活方式指南及效率工作技巧的优质中文科技生活类内容
    
    Args:
        tag: 分类
        limit: 返回结果数量限制
    
    Returns:
        null
    """
    arguments = {
        "tag": tag,
        "limit": limit
    }
    
    return call_api("1777419061629955", "get_sspai_rank", arguments)

def get_zhihu_trending(
    limit: Optional[int] = 50.0
) -> Dict[str, Any]:
    """
    获取知乎热榜，包含时事热点、社会话题、科技动态、娱乐八卦等多领域的热门问答和讨论的中文资讯
    
    Args:
        limit: 返回结果数量限制
    
    Returns:
        null
    """
    arguments = {
        "limit": limit
    }
    
    return call_api("1777419061629955", "get_zhihu_trending", arguments)

def get_douyin_trending(
) -> Dict[str, Any]:
    """
    获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_douyin_trending", arguments)

def get_hupu_trending(
) -> Dict[str, Any]:
    """
    获取虎扑热榜，包含虎扑体育赛事、步行街热帖、篮球足球话题及男性生活兴趣的热门中文讨论内容
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_hupu_trending", arguments)

def get_kuaishou_trending(
) -> Dict[str, Any]:
    """
    获取快手热榜，包含快手平台的热门短视频、热点话题及流行内容的实时热门中文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_kuaishou_trending", arguments)

def get_xiaohongshu_trending(
) -> Dict[str, Any]:
    """
    获取小红书热榜，包含小红书平台的热门笔记、时尚美妆、生活方式、种草推荐等热门中文内容
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_xiaohongshu_trending", arguments)

def get_9to5mac_news(
) -> Dict[str, Any]:
    """
    获取 9to5Mac 苹果相关新闻，包含苹果产品发布、iOS 更新、Mac 硬件、应用推荐及苹果公司动态的英文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_9to5mac_news", arguments)

def custom_rss(
) -> Dict[str, Any]:
    """
    自定义RSS订阅源
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "custom_rss", arguments)

def get_ifanr_news(
    limit: Optional[int] = 20.0,
    offset: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    获取爱范儿科技快讯，包含最新的科技产品、数码设备、互联网动态等前沿科技资讯
    
    Args:
        limit: 返回结果数量限制
        offset: 偏移量
    
    Returns:
        null
    """
    arguments = {
        "limit": limit,
        "offset": offset
    }
    
    return call_api("1777419061629955", "get_ifanr_news", arguments)

def get_gcores_new(
) -> Dict[str, Any]:
    """
    获取机核网游戏相关资讯，包含电子游戏评测、玩家文化、游戏开发和游戏周边产品的深度内容
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_gcores_new", arguments)

def get_smzdm_rank(
    unit: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    获取什么值得买热门，包含商品推荐、优惠信息、购物攻略、产品评测及消费经验分享的实用中文消费类资讯
    
    Args:
        unit: 时间范围：1(今日热门), 7(周热门), 30(月热门)
    
    Returns:
        null
    """
    arguments = {
        "unit": unit
    }
    
    return call_api("1777419061629955", "get_smzdm_rank", arguments)

def get_so360_trending(
) -> Dict[str, Any]:
    """
    获取360热搜榜，包含360搜索平台的热门搜索词、实时新闻热点及用户关注度较高的中文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_so360_trending", arguments)

def get_tencent_news_trending(
    page_size: Optional[int] = 20.0
) -> Dict[str, Any]:
    """
    获取腾讯新闻热点榜，包含国内外时事、社会热点、财经资讯、娱乐动态及体育赛事的综合性中文新闻资讯
    
    Args:
        page_size: 返回结果数量
    
    Returns:
        null
    """
    arguments = {
        "page_size": page_size
    }
    
    return call_api("1777419061629955", "get_tencent_news_trending", arguments)

def get_thepaper_trending(
) -> Dict[str, Any]:
    """
    获取澎湃新闻热榜，包含时政要闻、财经动态、社会事件、文化教育及深度报道的高质量中文新闻资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_thepaper_trending", arguments)

def get_theverge_news(
) -> Dict[str, Any]:
    """
    获取 The Verge 新闻，包含科技创新、数码产品评测、互联网趋势及科技公司动态的英文科技资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_theverge_news", arguments)

def get_toutiao_trending(
) -> Dict[str, Any]:
    """
    获取今日头条热榜，包含时政要闻、社会事件、国际新闻、科技发展及娱乐八卦等多领域的热门中文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_toutiao_trending", arguments)

def get_weibo_trending(
) -> Dict[str, Any]:
    """
    获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419061629955", "get_weibo_trending", arguments)

def get_weread_rank(
    category: Optional[str] = "rising"
) -> Dict[str, Any]:
    """
    获取微信读书排行榜，包含热门小说、畅销书籍、新书推荐及各类文学作品的阅读数据和排名信息
    
    Args:
        category: 排行榜分区：rising(飙升榜), hot_search(热搜榜), newbook(新书榜), general_novel_rising(小说榜), all(总榜)
    
    Returns:
        null
    """
    arguments = {
        "category": category
    }
    
    return call_api("1777419061629955", "get_weread_rank", arguments)

def crawl_website(
    url: str
) -> Dict[str, Any]:
    """
    爬取网站内容，多用于用户想要详细了解某网站内容时使用
    
    Args:
        url: 需要爬取的网站URL，多用于用户想要详细了解某网站内容时使用
    
    Returns:
        null
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777419061629955", "crawl_website", arguments)

