import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import requests
import time
import random

class StockAnalyzer:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.market = "sh" if stock_code.startswith("6") else "sz"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _request_with_retry(self, url, params=None, max_retries=5):
        """带重试的请求，避免被反爬"""
        for i in range(max_retries):
            try:
                # 随机延迟，模拟人类行为
                time.sleep(random.uniform(0.5, 2))
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    return response
                elif response.status_code in [403, 429]:
                    print(f"请求被限制，等待{2**i}秒后重试...")
                    time.sleep(2**i)
                else:
                    print(f"请求失败，状态码：{response.status_code}")
            except Exception as e:
                print(f"请求异常：{e}，等待{2**i}秒后重试...")
                time.sleep(2**i)
        raise Exception(f"请求失败，已重试{max_retries}次")

    def get_basic_info(self):
        """获取股票基础信息"""
        try:
            stock_info = ak.stock_individual_info_em(symbol=self.stock_code)
            info_dict = {}
            for _, row in stock_info.iterrows():
                info_dict[row['item']] = row['value']
            return info_dict
        except Exception as e:
            print(f"获取基础信息失败：{e}")
            return {}

    def get_realtime_quote(self):
        """获取实时行情数据"""
        try:
            # 尝试东方财富数据源
            stock_zh_a_spot = ak.stock_zh_a_spot_em()
            stock_data = stock_zh_a_spot[stock_zh_a_spot['代码'] == self.stock_code]
            if not stock_data.empty:
                return stock_data.iloc[0].to_dict()
            
            # 备用：新浪财经数据源
            url = f"https://hq.sinajs.cn/list={self.market}{self.stock_code}"
            response = self._request_with_retry(url)
            if response.text:
                data = response.text.split('"')[1].split(',')
                return {
                    "最新价": float(data[3]),
                    "涨跌幅": round((float(data[3]) - float(data[2]))/float(data[2])*100, 2),
                    "涨跌额": round(float(data[3]) - float(data[2]), 2),
                    "成交量": int(float(data[8])/100),  # 股转手
                    "成交额": float(data[9]),
                    "最高": float(data[4]),
                    "最低": float(data[5]),
                    "今开": float(data[1]),
                    "昨收": float(data[2]),
                    "量比": 0,  # 新浪接口不提供
                    "换手率": round(float(data[8])/float(info_dict['流通股'])*100, 2) if '流通股' in info_dict else 0,
                }
        except Exception as e:
            print(f"获取实时行情失败：{e}")
            return {}

    def get_kline_data(self, days=30):
        """获取K线数据"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
            
            # 尝试东方财富数据源
            stock_hist = ak.stock_zh_a_hist(
                symbol=self.stock_code, 
                period="daily", 
                start_date=start_date, 
                end_date=end_date, 
                adjust="qfq"
            )
            return stock_hist
        except Exception as e:
            print(f"获取K线数据失败：{e}")
            return pd.DataFrame()

    def get_fund_flow(self):
        """获取资金流向数据"""
        try:
            # 尝试东方财富数据源
            stock_moneyflow = ak.stock_individual_fund_flow(
                stock=self.stock_code, 
                market=self.market
            )
            if not stock_moneyflow.empty:
                return stock_moneyflow.iloc[0].to_dict()
            
            # 备用：东方财富网页版接口
            url = f"https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f104,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200&secid={1 if self.market == 'sh' else 0}.{self.stock_code}&cb=jQuery112406743224223325781_1709870000000&_=1709870000000"
            response = self._request_with_retry(url)
            # 解析JSONP数据
            import json
            data = json.loads(response.text[response.text.find('(')+1 : response.text.rfind(')')])
            if data and 'data' in data:
                flow_data = data['data']
                return {
                    "主力净流入-净额": flow_data.get('f62', 0),
                    "主力净流入-净占比": flow_data.get('f63', 0),
                    "超大单净流入-净额": flow_data.get('f66', 0),
                    "超大单净流入-净占比": flow_data.get('f67', 0),
                    "大单净流入-净额": flow_data.get('f70', 0),
                    "大单净流入-净占比": flow_data.get('f71', 0),
                    "中单净流入-净额": flow_data.get('f74', 0),
                    "中单净流入-净占比": flow_data.get('f75', 0),
                    "小单净流入-净额": flow_data.get('f78', 0),
                    "小单净流入-净占比": flow_data.get('f79', 0),
                }
        except Exception as e:
            print(f"获取资金流向失败：{e}")
            return {}

    def get_industry_info(self, industry_name):
        """获取行业板块数据"""
        try:
            # 获取行业板块行情 - 兼容不同版本的akshare
            try:
                board_data = ak.stock_board_industry_index_em(symbol=industry_name)
            except AttributeError:
                # 旧版本接口
                board_data = ak.stock_board_industry_name_em()
                board_data = board_data[board_data['板块名称'] == industry_name]
                if not board_data.empty:
                    board_code = board_data.iloc[0]['板块代码']
                    board_data = ak.stock_board_industry_hist_em(symbol=board_code, period="daily", start_date=(datetime.now()-timedelta(days=10)).strftime("%Y%m%d"), end_date=datetime.now().strftime("%Y%m%d"))
            
            if not board_data.empty:
                latest_data = board_data.iloc[-1]
                return {
                    "行业名称": industry_name,
                    "今日涨跌幅": latest_data.get('涨跌幅', 0),
                    "近5日涨跌幅": round(board_data.tail(5)['涨跌幅'].sum(), 2),
                    "近10日涨跌幅": round(board_data.tail(10)['涨跌幅'].sum(), 2),
                }
        except Exception as e:
            print(f"获取行业数据失败：{e}")
            return {}

    def get_announcements(self, days=7):
        """获取上市公司公告"""
        try:
            end_time = datetime.now().strftime("%Y-%m-%d")
            start_time = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            url = f"https://np-anotice.eastmoney.com/api/cgi-bin/announce?company={self.stock_code}&begin_time={start_time}&end_time={end_time}&page_size=10&page_index=1"
            response = self._request_with_retry(url)
            data = response.json()
            if data and 'data' in data and 'list' in data['data']:
                announcements = []
                for item in data['data']['list']:
                    announcements.append({
                        "标题": item.get('title', ''),
                        "发布时间": item.get('publish_time', ''),
                        "类型": item.get('announce_type', ''),
                    })
                return announcements
        except Exception as e:
            print(f"获取公告失败：{e}")
            return []

    def generate_report(self):
        """生成完整复盘报告"""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"# 新天然气(603393) 复盘报告 - {current_date}\n"
        report += "=" * 70 + "\n\n"

        # 1. 基础信息
        report += "## 一、基础信息\n"
        report += "-" * 50 + "\n"
        basic_info = self.get_basic_info()
        if basic_info:
            for key, value in basic_info.items():
                report += f"{key}: {value}\n"
        else:
            report += "基础信息获取失败\n"
        report += "\n"

        # 2. 实时行情
        report += "## 二、实时行情\n"
        report += "-" * 50 + "\n"
        quote = self.get_realtime_quote()
        if quote:
            report += f"最新价: {quote.get('最新价', 'N/A')} 元\n"
            report += f"涨跌幅: {quote.get('涨跌幅', 'N/A')} %\n"
            report += f"涨跌额: {quote.get('涨跌额', 'N/A')} 元\n"
            report += f"成交量: {quote.get('成交量', 'N/A')} 手\n"
            report += f"成交额: {quote.get('成交额', 'N/A')} 元\n"
            report += f"振幅: {quote.get('振幅', 'N/A')} %\n"
            report += f"最高: {quote.get('最高', 'N/A')} 元\n"
            report += f"最低: {quote.get('最低', 'N/A')} 元\n"
            report += f"今开: {quote.get('今开', 'N/A')} 元\n"
            report += f"昨收: {quote.get('昨收', 'N/A')} 元\n"
            report += f"量比: {quote.get('量比', 'N/A')}\n"
            report += f"换手率: {quote.get('换手率', 'N/A')} %\n"
            report += f"市盈率-动态: {quote.get('市盈率-动态', 'N/A')}\n"
            report += f"市净率: {quote.get('市净率', 'N/A')}\n"
            report += f"总市值: {quote.get('总市值', 'N/A')} 元\n"
            report += f"流通市值: {quote.get('流通市值', 'N/A')} 元\n"
        else:
            report += "实时行情获取失败\n"
        report += "\n"

        # 3. 近3日K线数据
        report += "## 三、近3日K线数据\n"
        report += "-" * 50 + "\n"
        kline = self.get_kline_data(days=3)
        if not kline.empty:
            report += kline[['日期', '开盘', '最高', '最低', '收盘', '涨跌幅', '成交量']].to_string(index=False) + "\n"
        else:
            report += "K线数据获取失败\n"
        report += "\n"

        # 4. 资金流向
        report += "## 四、资金流向\n"
        report += "-" * 50 + "\n"
        fund_flow = self.get_fund_flow()
        if fund_flow:
            report += f"主力净流入: {fund_flow.get('主力净流入-净额', 'N/A')} 元 ({fund_flow.get('主力净流入-净占比', 'N/A')} %)\n"
            report += f"超大单净流入: {fund_flow.get('超大单净流入-净额', 'N/A')} 元 ({fund_flow.get('超大单净流入-净占比', 'N/A')} %)\n"
            report += f"大单净流入: {fund_flow.get('大单净流入-净额', 'N/A')} 元 ({fund_flow.get('大单净流入-净占比', 'N/A')} %)\n"
            report += f"中单净流入: {fund_flow.get('中单净流入-净额', 'N/A')} 元 ({fund_flow.get('中单净流入-净占比', 'N/A')} %)\n"
            report += f"小单净流入: {fund_flow.get('小单净流入-净额', 'N/A')} 元 ({fund_flow.get('小单净流入-净占比', 'N/A')} %)\n"
        else:
            report += "资金流向获取失败\n"
        report += "\n"

        # 5. 行业板块
        report += "## 五、行业板块\n"
        report += "-" * 50 + "\n"
        industry_info = self.get_industry_info("燃气")
        if industry_info:
            report += f"所属行业: {industry_info.get('行业名称', '燃气')}\n"
            report += f"板块今日涨跌幅: {industry_info.get('今日涨跌幅', 'N/A')} %\n"
            report += f"板块近5日涨跌幅: {industry_info.get('近5日涨跌幅', 'N/A')} %\n"
        else:
            report += "行业板块数据获取失败\n"
        report += "\n"

        # 6. 近期公告
        report += "## 六、近期公告（近7日）\n"
        report += "-" * 50 + "\n"
        announcements = self.get_announcements(days=7)
        if announcements:
            for idx, ann in enumerate(announcements):
                report += f"{idx+1}. [{ann['发布时间']}] {ann['标题']}（{ann['类型']}）\n"
        else:
            report += "近7日无公告\n"
        report += "\n"

        report += "=" * 70 + "\n"
        report += f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        return report

if __name__ == "__main__":
    # 测试新天然气
    analyzer = StockAnalyzer("603393")
    report = analyzer.generate_report()
    print(report)