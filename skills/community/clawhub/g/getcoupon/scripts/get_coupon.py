#!/usr/bin/env python3
import urllib.request, json, sys, os, time, base64, hashlib, subprocess

# ============================================================
# 版本信息
# ============================================================
VERSION = "1.0.0"
SKILL_NAME = "getcoupon"
SKILL_PATH = os.path.expanduser(f"~/.openclaw/workspace/skills/{SKILL_NAME}")

# ============================================================
# 优惠券服务
# ============================================================
class CouponService:
    def __init__(self, query=""):
        self.query = query
        self.cache_file = "/tmp/coupon_data_cache"
        self.cache_ttl = 900
    
    def _get_api_config(self):
        # 原始配置
        # url: https://open.datadex.com.cn/dexserver/dex-api/v1/getcoupon
        # a1: APP-VENmEv0-938102249129914433-11
        # a2: KEY035VENnHsx2B3949IgMEfnaR4BWYGt93pedMkwpQ0v12
        
        # Base64 混淆加密：分割 + 混合
        # URL 片段
        url_part1 = "aHR0cHM6Ly9vcGVuLmRhdGFkZXguY29tLmNuL2RleHNlcnZlci9kZXgtYXBpL3Yx"
        url_part2 = "L2dldGNvdXBvbg=="
        
        # a1 (APP ID) 片段
        a1_part1 = "QVBQLVZFTm1FdjAtOTM4MTAy"
        a1_part2 = "MjQ5MTI5OTE0NDMzLTEx"
        
        # a2 (KEY) 片段
        a2_part1 = "S0VZMDM1VkVObkhzeA=="
        a2_part2 = "MkIzOTQ5SWdNRWZuYVI0QldZR3Q5M3BlZE1rd3BRMHYxMg=="
        
        # 重组
        api_base = base64.b64decode(url_part1).decode() + base64.b64decode(url_part2).decode()
        a1 = base64.b64decode(a1_part1).decode() + base64.b64decode(a1_part2).decode()
        a2 = base64.b64decode(a2_part1).decode() + base64.b64decode(a2_part2).decode()
        ts = str(int(time.time()))
        token = hashlib.md5(f"api_{ts}".encode()).hexdigest()[:8]
        
        return {
            'url': api_base,
            'a1': a1,
            'a2': a2,
            't1': ts,
            'token': token
        }
    
    def _decode_response(self, raw):
        return json.loads(raw)
    
    def get_cache(self):
        try:
            if os.path.exists(self.cache_file):
                mtime = os.path.getmtime(self.cache_file)
                if time.time() - mtime < self.cache_ttl:
                    with open(self.cache_file, 'r') as f:
                        return json.load(f)
        except:
            pass
        return None
    
    def set_cache(self, data):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    def _is_food_query(self):
        """判断是否是外卖/平台类查询"""
        if not self.query:
            return True
        food_keywords = ['外卖', '红包', '饿了', '美团', '吃饭', '点餐', '餐饮', '优惠券', '优惠', '省钱', '折扣', '平台']
        # 平台名称也归类为外卖/平台模式
        platform_keywords = ['京东', '拼多多', '淘宝', '闲鱼', '天猫', '美团', '饿了么', '抖音', '快手']
        q = self.query.lower()
        return any(k in q for k in food_keywords) or any(p in self.query for p in platform_keywords)
    
    def fetch_full_data(self):
        """获取完整数据（包含平台列表和类目列表）"""
        cached = self.get_cache()
        if cached:
            return {'data': cached, 'error': False, 'from_cache': True}
        
        config = self._get_api_config()
        api_url = config['url']
        
        payload = {
            'a1': config['a1'],
            'a2': config['a2'],
            't1': config['t1']
        }
        
        try:
            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                    'X-Token': config['token']
                },
                method='POST'
            )
            
            resp = urllib.request.urlopen(req, timeout=10)
            raw_data = resp.read().decode()
            data = self._decode_response(raw_data)
            
            if data.get('code') != 200:
                return {'data': None, 'error': True, 'error_msg': data.get('msg', '数据异常')}
            
            result_data = data.get('data', {})
            self.set_cache(result_data)
            return {'data': result_data, 'error': False, 'from_cache': False}
            
        except urllib.error.URLError as e:
            return {'data': None, 'error': True, 'error_msg': '网络连接失败'}
        except Exception as e:
            return {'data': None, 'error': True, 'error_msg': '数据获取失败'}
    
    def fetch(self):
        """兼容旧接口，返回过滤后的数据"""
        result = self.fetch_full_data()
        if result.get('error'):
            return result
        
        data = result.get('data', {})
        return {
            'data': self._filter(data),
            'error': False,
            'from_cache': result.get('from_cache', False)
        }
    
    def _filter(self, data):
        is_food = self._is_food_query()
        
        coupons = data.get('coupons', [])
        coupons = [c for c in coupons if c.get('status', 'active') == 'active']
        
        categories = data.get('categories', [])
        
        if is_food:
            if self.query:
                q = self.query.lower()
                coupons = [c for c in coupons if q in str(c.get('platform', '')).lower() 
                          or q in str(c.get('type', '')).lower()
                          or q in str(c.get('code', '')).lower()]
            return {'type': 'coupon', 'items': coupons}
        else:
            if self.query:
                q = self.query.lower()
                filtered = []
                for c in categories:
                    keywords = c.get('keywords', [])
                    category = c.get('category', '')
                    if q in category.lower() or any(q in k.lower() for k in keywords):
                        filtered.append(c)
                # 如果没有匹配到，返回空列表而不是返回所有
                categories = filtered
            return {'type': 'category', 'items': categories}
    
    def get_fallback_data(self):
        """返回兜底数据"""
        return {
            'type': 'coupon',
            'items': [
                {"platform": "饿了么", "type": "外卖红包", "discount": "最高20元", 
                 "code": "0复zんι此段1:/／UBsoNLI／~.👉淘宝闪购App👈【快來領外賣紅包，最高20元，人人都有哦~ https://to.ele.me/AK.cmUdmq3R_k?alsc_exsrc=ch_app_chsub_wordlink】", 
                 "tips": "复制本行消息，打开App即可领取", "weight": 100}
            ]
        }
    
    def get_all_platforms(self):
        """获取所有可用平台"""
        cached = self.get_cache()
        if cached:
            coupons = cached.get('coupons', [])
            platforms = list(set([c.get('platform', '未知') for c in coupons if c.get('status') == 'active']))
            return sorted(platforms)
        return []
    
    def get_all_categories(self):
        """获取所有商品类目"""
        cached = self.get_cache()
        if cached:
            categories = cached.get('categories', [])
            return [c.get('category', '未知') for c in categories if c.get('status') == 'active']
        return []

# ============================================================
# 升级检测
# ============================================================
def check_update():
    """检测并执行升级"""
    print(f"🔍 正在检测 {SKILL_NAME} 最新版本...\n")
    
    try:
        result = subprocess.run(
            ["clawhub", "update", SKILL_NAME],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 升级成功！最新版本来啦～\n")
            print("请重新尝试查询优惠，如「外卖优惠」\n")
            return True
        else:
            print(f"⚠️ 升级失败：{result.stderr or result.stdout}")
            return False
            
    except FileNotFoundError:
        print("⚠️ 未找到 clawhub 命令，请先安装 clawhub CLI")
        print("   npm i -g clawhub\n")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️ 升级超时，请稍后重试\n")
        return False
    except Exception as e:
        print(f"⚠️ 升级异常：{str(e)}\n")
        return False

def show_version():
    """显示当前版本"""
    print(f"{SKILL_NAME} v{VERSION}\n")

# ============================================================
# 主函数
# ============================================================
def main():
    args = sys.argv[1:]
    
    # 处理特殊命令
    if "--version" in args or "-v" in args:
        show_version()
        return
    
    if "--check-update" in args or "--upgrade" in args or "升级" in "".join(args):
        check_update()
        return
    
    # 正常查询
    query = " ".join(args) if args else ""
    svc = CouponService(query)
    
    # 无查询词时，显示概览
    if not query or query in ['优惠', '有什么优惠', '查看优惠']:
        result = svc.fetch_full_data()
        
        if result.get('error'):
            print(f"⚠️ 数据爬取失败，请稍后重试。\n")
            print("─" * 40)
            print("💡 如问题持续，请告诉我「升级最新版」\n")
            return
        
        # 显示平台列表
        platforms = svc.get_all_platforms()
        categories = svc.get_all_categories()
        
        print("🏪 当前可用优惠平台：\n")
        for i, p in enumerate(platforms, 1):
            print(f"   {i}. {p}")
        
        if categories:
            print(f"\n🛍️ 检测到 {len(categories)} 个商品类目优惠，部分展示：\n")
            # 展示前5个类目
            for i, c in enumerate(categories[:5], 1):
                print(f"   {i}. {c}")
            
            if len(categories) > 5:
                print(f"   ... 等共 {len(categories)} 个类目")
            
            print("\n💡 请告诉我您想要的，如：")
            print("   • 「手机优惠」")
            print("   • 「衣服」")
            print("   • 「外卖红包」")
            print("   • 直接输入平台名称，如「饿了么」「美团」\n")
        return
    
    # 有查询词，走原有逻辑
    result = svc.fetch()
    
    if result.get('error'):
        print(f"⚠️ 数据爬取失败，请稍后重试。\n")
        fallback_result = svc.get_fallback_data()
        items = fallback_result.get('items', [])
        
        if fallback_result['type'] == 'coupon':
            print("🎁 为您找到以下外卖优惠：\n")
            for i, item in enumerate(items[:3], 1):
                platform = item.get('platform', '未知')
                discount = item.get('discount', '未知')
                code = item.get('code', '')
                tips = item.get('tips', '')
                print(f"{i}. 【{platform}】{discount}")
                print(f"   复制打开App：[ {code} ]")
                print(f"   使用方法：{tips}")
                print("")
        
        print("─" * 40)
        print("💡 如问题持续，请告诉我「升级最新版」\n")
        return
    
    data = result.get('data', {})
    items = data.get('items', [])
    
    if not items:
        print("暂无相关优惠，换个关键词试试？")
        return
    
    items = sorted(items, key=lambda x: x.get('weight', 0), reverse=True)
    
    if data.get('type') == 'coupon':
        print("🎁 为您找到以下优惠：\n")
        
        for i, item in enumerate(items[:3], 1):
            platform = item.get('platform', '未知')
            discount = item.get('discount', '未知')
            code = item.get('code', '')
            tips = item.get('tips', '')
            is_top = item.get('weight', 0) >= 90
            star = " ⭐推荐" if is_top and i == 1 else ""
            print(f"{i}. 【{platform}】{discount}{star}")
            print(f"   复制打开App：[ {code} ]")
            print(f"   使用方法：{tips}")
            print("")
        
        if len(items) > 1:
            print(f"💡 {items[0].get('platform')} 优惠力度更大，推荐这个！\n")
    else:
        print("🛍️ 为您找到以下商品优惠：\n")
        
        for i, item in enumerate(items[:3], 1):
            category = item.get('category', '未知')
            title = item.get('title', '')
            platform = item.get('platform', '')
            discount = item.get('discount', '')
            link = item.get('link', '')
            tips = item.get('tips', '')
            is_top = item.get('weight', 0) >= 90
            star = " ⭐推荐" if is_top and i == 1 else ""
            print(f"{i}. {category} - {title}{star}")
            print(f"   平台：{platform} | 优惠：{discount}")
            print(f"   👉 {link}")
            print(f"   使用方法：{tips}")
            print("")
    
    print("❓ 领取失败？尝试以下方法：")
    print("   • 确保App已更新到最新版本")
    print("   • 复制完整链接后重新打开")
    print("   • 换个时间段再试试\n")
    
    print("有问题随时问我～")

if __name__ == "__main__":
    main()
