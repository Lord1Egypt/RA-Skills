# 导入自动化模块（核心：页面操作+接口监听）
import time
import re

from DrissionPage import ChromiumPage, ChromiumOptions
# 格式化输出（方便调试，查看数据结构）
from pprint import pprint
# 导入csv模块（处理CSV文件写入）
import csv


def parse_month_salary(s):
    if not s or "面议" in s:
        return None

    # 忽略按天/周薪
    if "元/天" in s or "元/周" in s:
        return None

    # 提取 K 区间
    m = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*K", s, re.I)
    if not m:
        return None

    low = float(m.group(1)) * 1000
    high = float(m.group(2)) * 1000

    return (low+high)/2


def crawl_boss_zhipin():
    # 1. 初始化CSV文件，配置表头和写入对象
    with open('boss.csv', mode='w', encoding='utf-8', newline='') as f:
        # 定义CSV文件表头字段
        csv_fieldnames = [
            '岗位名称',
            '公司',
            '规模',
            '公司领域',
            '学历要求',
            '经验要求',
            '技能需求',
            '福利待遇',
            '薪资',
            '市',
            '区',
            '商圈',
            '经度',
            '纬度'
        ]
        # 初始化DictWriter对象（用于字典格式数据写入）
        csv_writer = csv.DictWriter(f, fieldnames=csv_fieldnames)
        # 写入CSV表头
        csv_writer.writeheader()

        # 2. 初始化浏览器对象，开启接口监听
        # dp = ChromiumPage()
        co = ChromiumOptions()
        co.debugger_address = '127.0.0.1:9222'
        dp = ChromiumPage(co)

        # 监听接口关键词：joblis
        # t（匹配BOSS直聘岗位列表接口）
        dp.listen.start('joblist')
        # 访问BOSS直聘大数据开发岗位页面（city=101280600 对应深圳，可修改城市编码，101020100上海）
        target_url = "https://www.zhipin.com/web/geek/jobs?query=%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B7%A5%E7%A8%8B%E5%B8%88&city=101020100"
        dp.get(target_url)

        # 3. 循环翻页，爬取前20页数据
        total_pages = 1
        for page in range(1, total_pages + 1):
            print(f'========== 正在采集第{page}页数据内容 ==========')
            try:
                # 等待接口数据包返回（超时时间默认30秒，可调整）
                resp = dp.listen.wait(timeout=5)
                # 获取接口返回的JSON数据
                json_data = resp.response.body
                # 4. 提取岗位列表数据，解析并写入CSV
                # 从JSON数据中提取岗位列表（核心数据节点）
                job_list = json_data['zpData']['jobList']
                print(job_list)
                for job in job_list:
                    # 构造单条岗位数据字典
                    job_info = {
                        '岗位名称': job.get('jobName', ''),
                        '公司': job.get('brandName', ''),
                        '规模': job.get('brandScaleName', ''),
                        '公司领域': job.get('brandIndustry', ''),
                        '学历要求': job.get('jobDegree', ''),
                        '经验要求': job.get('jobExperience', ''),
                        '技能需求': job.get('skills', []),
                        '福利待遇': job.get('welfareList', []),
                        '薪资': parse_month_salary(job.get('salaryDesc', '')),
                        '市': job.get('cityName', ''),
                        '区': job.get('areaDistrict', ''),
                        '商圈': job.get('businessDistrict', ''),
                        '经度': job.get('gps', {}).get('longitude', ''),
                        '纬度': job.get('gps', {}).get('latitude', '')
                    }

                    # 写入单条岗位数据到CSV
                    csv_writer.writerow(job_info)
                    # 格式化输出当前爬取的岗位信息（方便查看进度）
                    pprint(job_info)

                # 5. 页面下滑到底部，触发下一页数据加载（核心翻页逻辑）
                dp.scroll.to_bottom()

            except Exception as e:
                print(f'第{page}页数据采集失败，错误信息：{str(e)}')
                continue
            time.sleep(5)
        # 6. 爬取完成，关闭浏览器
        # dp.quit()
        print(f'========== 全部{total_pages}页数据采集完成，结果已存入boss.csv ==========')


if __name__ == '__main__':
    crawl_boss_zhipin()