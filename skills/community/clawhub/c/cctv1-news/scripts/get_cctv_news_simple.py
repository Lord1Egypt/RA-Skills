import requests
import datetime
import pytz
import os
import time
from lxml import etree

"""
简单版CCTV新闻联播获取脚本
功能：获取CCTV新闻联播内容并保存到本地文件
无需钉钉机器人配置
"""

def get_current_time():
    """获取当前时间"""
    current_time = datetime.datetime.now()
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = current_time.astimezone(beijing_tz)
    date_format = beijing_time.strftime('%Y%m%d')
    return date_format


def parse_html(url):
    """解析HTML页面"""
    try:
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        return html
    except Exception as e:
        print(f"解析HTML失败: {e}")
        return None


def get_cctv_news():
    """获取CCTV新闻联播内容"""
    url1 = "https://tv.cctv.com/lm/xwlb/"
    html = parse_html(url1)
    
    if html is None:
        print("无法获取CCTV主页内容")
        return None
    
    # 获取新闻章节数量
    xpath = 'count(//*[@id="content"]/li)'
    try:
        count = int(html.xpath(xpath))
    except:
        print("无法获取新闻章节数量")
        return None
    
    date = get_current_time()
    arry_text = []
    
    # 循环获取每个视频的内容
    for i in range(1, count + 1):
        try:
            xpath2 = '//*[@id="content"]/li[{}]/div/a/@href'.format(i) 
            urls = html.xpath(xpath2)
            
            for url2 in urls:
                if not url2:
                    continue
                    
                sub_html = parse_html(url2) 
                if sub_html is None:
                    continue
                
                if i == 1:
                    # 第一个是完整版视频
                    url = "[完整版视频链接]({})".format(urls[0])
                    arry_text.append(url + '\n')
                else:
                    # 其他是章节摘要
                    xpath3 = '//*[@id="page_body"]/div[1]/div[2]/div[2]/div[2]/div/ul/li[1]/p/text()'
                    content3 = sub_html.xpath(xpath3)
                    if content3:
                        content3 = '[节摘要：' + ''.join(content3) + ']({})'.format(url2)
                        arry_text.append(content3 + '\n')
        except Exception as e:
            print(f"处理第{i}个章节时出错: {e}")
            continue
    
    return date, arry_text


def save_to_file(date, content_list):
    """保存内容到文件"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 生成文件名
    filename = f"cctv_news_{date}.txt"
    filepath = os.path.join(script_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{date} 新闻联播\n")
            f.write("=" * 50 + "\n\n")
            for item in content_list:
                f.write(item)
        
        print(f"新闻内容已保存到: {filepath}")
        return filepath
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return None


def main():
    """主执行函数"""
    print(f"开始获取CCTV新闻联播内容...")
    
    # 获取新闻联播内容
    result = get_cctv_news()
    if result is None:
        print("无法获取新闻联播内容")
        return
    
    date, arry_text = result
    
    # 保存到文件
    save_to_file(date, arry_text)
    
    print(f"完成！获取到 {len(arry_text)} 条新闻内容")


if __name__ == "__main__":
    main()