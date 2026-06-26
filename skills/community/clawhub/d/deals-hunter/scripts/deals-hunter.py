#!/usr/bin/env python3
"""
deals-hunter v6.0
品类过滤 + 黑名单 + 历史价缓存 + Tavily 多 key 轮询 + 配额控制
数据源: 什么值得买 RSS
"""

import feedparser
import requests
import json
import os
import re
from datetime import datetime, timezone

class DealsHunter:
    def __init__(self):
        self.all_deals = []
        self.dedup_file = '/Users/xufan65/.openclaw/workspace/memory/deals-sent.json'
        self.price_cache_file = '/Users/xufan65/.openclaw/workspace/memory/deals-price-cache.json'
        
        # Tavily 多 key 轮询
        keys_str = os.environ.get('TAVILY_API_KEYS', '')
        self.tavily_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        if not self.tavily_keys:
            single = os.environ.get('TAVILY_API_KEY', '')
            if single:
                self.tavily_keys = [single]
        self.tavily_index = 0
        self._quota_exhausted = False  # 配额耗尽标记
        
        # 品类过滤关键词
        self.category_keywords = {
            '数码电子': [
                '手机', '平板', '耳机', '充电器', '充电宝', '数据线', '蓝牙', '音箱',
                '智能手表', '手环', '相机', '无人机', '投影仪', '路由器',
                'iPhone', 'iPad', 'AirPods', 'MacBook', 'Galaxy', 'Pixel',
                'Sony', 'BOSE', 'JBL', 'Anker', 'ANKER', '充电', 'Type-C',
                'USB-C', '快充', '无线充', '移动电源', '储存卡', 'SD卡', 'TF卡',
                'Switch', 'PS5', 'Xbox', '显示器', '机械键盘', '鼠标', '摄像头',
                '运动相机', 'GoPro', 'DJI', '大疆', 'Kindle', '电子书',
            ],
            '电脑办公': [
                '笔记本', '台式机', '显示器', '显卡', 'CPU', '内存条', '固态硬盘',
                'SSD', 'HDD', '机械键盘', '鼠标', '路由器', 'NAS', 'UPS',
                '打印机', '扫描仪', '投影仪', '硬盘', 'U盘', '扩展坞',
                '主板', '散热器', '电源', '机箱', '网线', '交换机',
                'MacBook', 'ThinkPad', 'Surface', '雷蛇', '罗技', 'Logitech',
                'Razer', 'HHKB', 'Cherry', '联想', '戴尔', 'DELL', '华硕',
                'ASUS', '微星', 'MSI', '技嘉', 'WD', '西数', '三星', 'Samsung',
                'Kingston', '金士顿', ' Crucial', '英睿达', '希捷', 'Seagate',
                'Synology', '群晖', '威联通', 'QNAP',
            ],
            '智能家居': [
                '扫地机器人', '智能灯', '智能门锁', '空气净化器', '加湿器',
                '智能插座', '智能开关', '智能窗帘', '智能马桶', '净水器',
                '新风机', '除湿机', '洗碗机', '烘干机', '洗衣机',
                '智能音箱', '智能门铃', '监控', '摄像头', '传感器',
                'HomeKit', '米家', 'Aqara', '涂鸦', '石头', 'Roborock',
                '追觅', 'Dreame', '科沃斯', 'Ecovacs', 'iRobot',
                '戴森', 'Dyson', '飞利浦', 'Philips', 'Yeelight', '涂鸦',
                '博世', '西门子', '松下', 'Panasonic', '美的', '海尔', '格力',
                '净水', '滤芯', '除螨仪', '蒸汽拖把', '擦窗机器人',
            ],
            '日用零食': [
                '零食', '咖啡', '茶', '牛奶', '酸奶', '啤酒', '白酒', '红酒',
                '巧克力', '坚果', '饼干', '方便面', '面条', '大米', '食用油',
                '纸巾', '洗衣液', '洗洁精', '沐浴露', '洗发水', '牙膏', '牙刷',
                '面膜', '护肤品', '防晒霜', '卸妆', '洗衣凝珠', '消毒液',
                '垃圾袋', '保鲜膜', '拖把', '洗碗巾', '洁厕剂', '柔顺剂',
                '保温杯', '水杯', '电水壶', '雨伞', '刀具',
                '三只松鼠', '良品铺子', '百草味', '伊利', '蒙牛', '农夫山泉',
                '可口可乐', '百事', '星巴克', 'Nespresso', '雀巢', '瑞幸',
                '元气森林', '认养一头牛', '金龙鱼', '福临门', '蓝月亮', '立白',
                '维达', '清风', '心相印', '全棉时代', '花王', '狮王',
                '欧莱雅', 'L\'Oreal', '妮维雅', 'Nivea', '高露洁', 'Colgate',
                '舒肤佳', 'Safeguard', '滴露', 'Dettol', '威露士',
            ],
            '食品生鲜': [
                '水果', '蔬菜', '肉类', '海鲜', '鸡蛋', '面粉', '调味料',
                '酱油', '醋', '料酒', '番茄酱', '蜂蜜', '燕麦', '麦片',
                '牛排', '鸡翅', '三文鱼', '虾仁', '排骨', '牛肉', '猪肉',
                '苹果', '橙子', '草莓', '蓝莓', '芒果', '榴莲', '车厘子',
            ],
            '个护美妆': [
                '口红', '粉底', '眼影', '眉笔', '睫毛膏', '遮瑕', '定妆',
                '爽肤水', '精华', '面霜', '乳液', '眼霜', '卸妆水', '洗面奶',
                '香水', '香氛', '发膜', '护发素', '身体乳', '磨砂膏',
                '卫生巾', '安全套', '成人用品',
            ],
            '家用电器': [
                '电饭煲', '微波炉', '烤箱', '空气炸锅', '电压力锅', '电磁炉',
                '电热水壶', '豆浆机', '破壁机', '榨汁机', '搅拌机',
                '吸尘器', '蒸汽拖把', '挂烫机', '电熨斗', '缝纫机',
                '电风扇', '取暖器', '加湿器', '电热毯', '电蚊香',
                '苏泊尔', '美的', '九阳', '松下', '飞利浦', '小熊',
            ],
        }
        self.enabled_categories = ['数码电子', '电脑办公', '智能家居', '日用零食', '食品生鲜', '个护美妆', '家用电器']
        
        # 黑名单：过滤非商品内容
        self.spam_keywords = [
            '抽奖', '转发', '关注领', '签到', '京豆', '领券', '领红包',
            'PLUS会员', 'plus会员', '满减门槛', '活动入口', '口令',
            '免费领', '0元', '0.01元', '免费送', '限量抢', '预约',
        ]
    
    def is_spam_or_activity(self, title, description=''):
        """过滤抽奖、活动、京豆等非商品内容"""
        text = (title + ' ' + description).lower()
        for kw in self.spam_keywords:
            if kw.lower() in text:
                return True
        return False
    
    def matches_category(self, title, description=''):
        """检查商品是否匹配关注品类"""
        if not self.enabled_categories:
            return True, None
        
        text = (title + ' ' + description).lower()
        for cat in self.enabled_categories:
            keywords = self.category_keywords.get(cat, [])
            for kw in keywords:
                if kw.lower() in text:
                    return True, cat
        
        return False, None
        
    def load_sent_deals(self):
        try:
            with open(self.dedup_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_sent_deals(self, sent_deals):
        os.makedirs(os.path.dirname(self.dedup_file), exist_ok=True)
        with open(self.dedup_file, 'w', encoding='utf-8') as f:
            json.dump(sent_deals, f, ensure_ascii=False, indent=2)
    
    def load_price_cache(self):
        try:
            with open(self.price_cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_price_cache(self, cache):
        os.makedirs(os.path.dirname(self.price_cache_file), exist_ok=True)
        with open(self.price_cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def get_cached_price(self, title):
        cache = self.load_price_cache()
        key = title[:40]
        entry = cache.get(key)
        if not entry:
            return None
        # 缓存 24h 有效
        try:
            cached_time = datetime.fromisoformat(entry['time'])
            if (datetime.now(timezone.utc) - cached_time).total_seconds() < 86400:
                return entry
        except:
            pass
        return None
    
    def set_cached_price(self, title, price_info):
        cache = self.load_price_cache()
        key = title[:40]
        cache[key] = {
            'time': datetime.now(timezone.utc).isoformat(),
            'data': price_info,
        }
        # 只保留最近 200 条
        if len(cache) > 200:
            cache = dict(list(cache.items())[-200:])
        self.save_price_cache(cache)
    
    def _get_tavily_key(self):
        """轮询获取下一个 Tavily key"""
        if not self.tavily_keys:
            return None
        key = self.tavily_keys[self.tavily_index % len(self.tavily_keys)]
        self.tavily_index += 1
        return key
    
    def _tavily_request(self, payload):
        """带多 key 重试的 Tavily 请求"""
        max_attempts = len(self.tavily_keys) or 1
        for attempt in range(max_attempts):
            key = self._get_tavily_key()
            if not key:
                return None
            payload['api_key'] = key
            try:
                resp = requests.post("https://api.tavily.com/search", json=payload, timeout=15)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code in (429, 432):
                    print(f"   ⚠️ Key {key[:20]}... 配额耗尽({resp.status_code})，切换下一个")
                    continue
                else:
                    print(f"   ⚠️ Tavily 返回 {resp.status_code}")
                    return None
            except Exception as e:
                print(f"   ⚠️ Tavily 请求失败: {e}")
                continue
        # 所有 key 都耗尽
        self._quota_exhausted = True
        print(f"   ⚠️ 所有 Tavily key 配额耗尽，跳过历史价查询")
        return None
    
    def fetch_smzdm_rss(self):
        """获取什么值得买 RSS"""
        print("\n📡 数据源 1: 什么值得买 RSS")
        try:
            feed = feedparser.parse("http://feed.smzdm.com")
            print(f"✅ 获取 {len(feed.entries)} 条优惠")
            
            count = 0
            skipped = 0
            for entry in feed.entries[:50]:
                title = entry.title
                link = entry.link
                description = entry.get('description', '')
                
                # 黑名单过滤（先过滤，减少误判）
                if self.is_spam_or_activity(title, description):
                    skipped += 1
                    continue
                
                # 品类过滤
                matched, category = self.matches_category(title, description)
                if not matched:
                    skipped += 1
                    continue
                
                # 提取价格
                price_match = re.search(r'(\d+\.?\d*)\s*元', title + ' ' + description)
                price = float(price_match.group(1)) if price_match else None
                
                self.all_deals.append({
                    'source': '什么值得买',
                    'title': title,
                    'link': link,
                    'description': description[:200],
                    'price': price,
                    'published': entry.get('published', ''),
                    'category': category,
                })
                count += 1
            
            print(f"   ✅ 添加 {count} 个优惠（过滤掉 {skipped} 个不相关商品）")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            return False
    
    def extract_prices_from_text(self, text):
        """从文本中提取所有价格"""
        prices = []
        patterns = [
            r'[¥￥]\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*[元块]',
            r'价格[：:]*\s*[¥￥]?\s*(\d+\.?\d*)',
            r'价\s*[¥￥]?\s*(\d+\.?\d*)',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                price = float(match.group(1))
                if 1 < price < 100000:
                    prices.append(price)
        return prices

    def search_price_history(self, deal):
        """搜索商品历史价格（多 key 轮询 + 缓存 + 配额控制）"""
        # 配额耗尽直接跳过
        if self._quota_exhausted:
            return None
        
        # 先查缓存
        cached = self.get_cached_price(deal['title'])
        if cached:
            print(f"   📦 使用缓存数据")
            return cached.get('data')
        
        try:
            # 清理标题
            clean_title = deal['title']
            for noise in ['到手价', '券后价', '限时', '秒杀', '爆款', '直降', '满减', '补贴', '【', '】', '（需用券）']:
                clean_title = clean_title.replace(noise, ' ')
            clean_title = re.sub(r'[¥￥]\s*\d+\.?\d*', '', clean_title)
            clean_title = re.sub(r'\d+\.?\d*元', '', clean_title)
            clean_title = re.sub(r'\s+', ' ', clean_title).strip()
            
            price_info = {
                'current_price': deal.get('price'),
                'original_price': None,
                'lowest_price': None,
                'lowest_date': None,
                'purchase_link': None,
                'manmanbuy_link': None,
                'source': None
            }
            
            # 策略1：搜慢慢买
            payload1 = {
                "query": f'"{clean_title[:25]}" 历史最低价',
                "search_depth": "advanced",
                "max_results": 5,
            }
            data = self._tavily_request(payload1)
            
            if data:
                for result in data.get('results', []):
                    content = result.get('content', '')
                    result_url = result.get('url', '')
                    
                    if 'manmanbuy' in result_url and not price_info['manmanbuy_link']:
                        price_info['manmanbuy_link'] = result_url
                    
                    # 提取最低价
                    for pattern in [r'历史最低[价格]*[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'最低价[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'史低[：:]*\s*[¥￥]?\s*(\d+\.?\d*)']:
                        if not price_info['lowest_price']:
                            match = re.search(pattern, content)
                            if match:
                                p = float(match.group(1))
                                if 1 < p < 100000:
                                    price_info['lowest_price'] = p
                    
                    # 提取当前价
                    for pattern in [r'当前价[格]*[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'现价[：:]*\s*[¥￥]?\s*(\d+\.?\d*)']:
                        if not price_info['current_price']:
                            match = re.search(pattern, content)
                            if match:
                                p = float(match.group(1))
                                if 1 < p < 100000:
                                    price_info['current_price'] = p
                    
                    # 提取原价
                    for pattern in [r'原价[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'定价[：:]*\s*[¥￥]?\s*(\d+\.?\d*)']:
                        if not price_info['original_price']:
                            match = re.search(pattern, content)
                            if match:
                                p = float(match.group(1))
                                if 1 < p < 100000:
                                    price_info['original_price'] = p
                    
                    # 提取日期
                    if price_info['lowest_price'] and not price_info['lowest_date']:
                        date_match = re.search(r'(\d{4}[-年/]\d{1,2}[-月/]\d{1,2})', content)
                        if date_match:
                            price_info['lowest_date'] = date_match.group(1)
                    
                    if price_info['lowest_price']:
                        break
            
            # 策略2：没找到则扩大搜索
            if not price_info['lowest_price'] and not self._quota_exhausted:
                payload2 = {
                    "query": f"{clean_title[:30]} 京东 历史最低价 价格走势",
                    "search_depth": "basic",
                    "max_results": 3,
                }
                data2 = self._tavily_request(payload2)
                if data2:
                    for result in data2.get('results', []):
                        content = result.get('content', '')
                        result_url = result.get('url', '')
                        if not price_info['lowest_price']:
                            for pattern in [r'历史最低[价格]*[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'最低价[：:]*\s*[¥￥]?\s*(\d+\.?\d*)', r'史低[：:]*\s*[¥￥]?\s*(\d+\.?\d*)']:
                                match = re.search(pattern, content)
                                if match:
                                    p = float(match.group(1))
                                    if 1 < p < 100000:
                                        price_info['lowest_price'] = p
                                        break
                        if 'jd.com' in result_url and not price_info['purchase_link']:
                            price_info['purchase_link'] = result_url
                            price_info['source'] = '京东'
                        elif 'tmall.com' in result_url and not price_info['purchase_link']:
                            price_info['purchase_link'] = result_url
                            price_info['source'] = '天猫'
                        if 'manmanbuy' in result_url and not price_info['manmanbuy_link']:
                            price_info['manmanbuy_link'] = result_url
            
            # 兜底链接
            if not price_info['purchase_link']:
                price_info['purchase_link'] = deal['link']
                price_info['source'] = '什么值得买'
            if not price_info['manmanbuy_link']:
                search_term = clean_title[:20].replace(' ', '+')
                price_info['manmanbuy_link'] = f"https://cu.manmanbuy.com/search.php?s={search_term}"
            
            # 写入缓存
            self.set_cached_price(deal['title'], price_info)
            return price_info
                
        except Exception as e:
            print(f"   ⚠️ 搜索失败: {e}")
            return None
    
    def generate_buy_advice(self, price_info, deal):
        """生成购买建议（详细版）"""
        advice = {
            'recommendation': None,
            'reason': None,
            'timing': None,
            'savings': None,
            'price_comparison': None,
            'action_tip': None
        }
        
        # 处理 price_info 为 None 的情况
        if price_info is None:
            price_info = {}
        
        current_price = price_info.get('current_price') or deal.get('price')
        lowest_price = price_info.get('lowest_price')
        
        if not current_price:
            advice['recommendation'] = '🔍 查看详情'
            advice['reason'] = '无法获取价格信息'
            advice['action_tip'] = '点击链接查看实际价格'
            return advice
        
        # 如果没有历史最低价，使用保守建议
        if not lowest_price:
            advice['recommendation'] = '🤔 暂无参考'
            advice['reason'] = '未找到历史价格数据'
            advice['action_tip'] = '🔍 建议查看详情页或对比其他平台'
            price_info['lowest_price_note'] = ''
            return advice
        
        # 计算价差
        price_diff = current_price - lowest_price
        price_pct = (price_diff / lowest_price) * 100 if lowest_price > 0 else 0
        
        advice['savings'] = f"¥{price_diff:.0f}"
        advice['price_comparison'] = f"当前 ¥{current_price} vs 最低 ¥{lowest_price}"
        
        # 生成详细建议
        if price_pct <= 5:
            advice['recommendation'] = '✅ 建议入手'
            advice['reason'] = f'差价仅 ¥{price_diff:.0f}，接近史低'
            advice['timing'] = '现在'
            advice['action_tip'] = '🎯 好价，可以入手'
        elif price_pct <= 15:
            advice['recommendation'] = '💡 可以考虑'
            advice['reason'] = f'差价 ¥{price_diff:.0f}，高出 {price_pct:.1f}%'
            advice['timing'] = '不急可等'
            advice['action_tip'] = '⏳ 急用可买，不急等促销'
        elif price_pct <= 30:
            advice['recommendation'] = '⏰ 建议等待'
            advice['reason'] = f'差价 ¥{price_diff:.0f}，高出 {price_pct:.1f}%'
            advice['timing'] = '等待促销'
            advice['action_tip'] = '💰 等 618/双11 更划算'
        else:
            advice['recommendation'] = '❌ 不建议购买'
            advice['reason'] = f'差价 ¥{price_diff:.0f}，高出 {price_pct:.1f}%'
            advice['timing'] = '等待大促'
            advice['action_tip'] = '🚫 价格偏高，建议观望'
        
        return advice
    
    def generate_detailed_report(self):
        """生成增强版羊毛推荐报告（含历史最低价和购买建议）"""
        print("\n" + "=" * 60)
        print("📊 生成增强版报告（含历史最低价 + 购买建议）...")
        print("=" * 60)
        
        # 去重（12h 窗口）
        sent_deals = self.load_sent_deals()
        now = datetime.now(timezone.utc)
        dedup_window = 12 * 3600  # 12小时
        
        new_deals = []
        for deal in self.all_deals:
            deal_key = deal['title'][:50]
            if deal_key not in sent_deals:
                new_deals.append(deal)
            else:
                try:
                    sent_time = datetime.fromisoformat(sent_deals[deal_key])
                    elapsed = (now - sent_time).total_seconds()
                    if elapsed > dedup_window:
                        new_deals.append(deal)
                except:
                    new_deals.append(deal)
        
        if not new_deals:
            print("\n⚠️  没有新的优惠商品")
            return None
        
        # 选择前 15 个商品
        top_deals = new_deals[:15]
        # 只对前 5 个查历史价（节省 Tavily 配额）
        price_check_limit = 5
        
        # 生成报告
        report_lines = []
        report_lines.append(f"**🐑 今日羊毛推荐（增强版）** - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append("")
        report_lines.append(f"📦 商品数量: {len(top_deals)} | 📊 含历史最低价 + 购买建议")
        report_lines.append("")
        report_lines.append("---")
        
        # 统计
        buy_now_count = 0
        wait_count = 0
        
        # 添加每个商品的详细信息
        for i, deal in enumerate(top_deals, 1):
            print(f"\n🔍 处理 {i}/{len(top_deals)}: {deal['title'][:30]}...")
            
            # 只对前 N 个查历史价
            if i <= price_check_limit:
                price_info = self.search_price_history(deal)
            else:
                price_info = None
            
            # 生成购买建议
            advice = self.generate_buy_advice(price_info, deal)
            
            if '✅' in advice['recommendation']:
                buy_now_count += 1
            elif '⏰' in advice['recommendation'] or '❌' in advice['recommendation']:
                wait_count += 1
            
            # 添加商品信息
            report_lines.append("")
            report_lines.append(f"**{i}. {deal['title']}**")
            report_lines.append("")
            
            # 价格对比
            current_price = price_info.get('current_price') if price_info else deal.get('price')
            lowest_price = price_info.get('lowest_price') if price_info else None
            original_price = price_info.get('original_price') if price_info else None
            
            # 当前价格和历史最低价
            if current_price:
                report_lines.append(f"💰 当前价格: **¥{current_price}**")
            
            if lowest_price:
                note = price_info.get('lowest_price_note', '')
                report_lines.append(f"📉 历史最低价: **¥{lowest_price}** {note}")
                
                # 计算差价
                price_diff = current_price - lowest_price if current_price else 0
                if price_diff > 0:
                    price_pct = (price_diff / lowest_price) * 100
                    report_lines.append(f"📊 价格对比: 比史低高 **¥{price_diff:.0f}** ({price_pct:.1f}%)")
            elif current_price:
                report_lines.append(f"📉 历史最低价: 暂无数据")
            
            # 原价（如果有）
            if original_price and original_price > current_price:
                discount_pct = ((original_price - current_price) / original_price) * 100
                report_lines.append(f"🏷️ 原价: ¥{original_price}（立省 {discount_pct:.0f}%）")
            
            # 购买建议（详细版）
            report_lines.append("")
            report_lines.append(f"💡 购买建议: **{advice['recommendation']}**")
            if lowest_price:  # 有历史价格才显示详细建议
                report_lines.append(f"   ├─ {advice['reason']}")
                if advice.get('action_tip'):
                    report_lines.append(f"   └─ {advice['action_tip']}")
            else:  # 没有历史价格，简化建议
                report_lines.append(f"   └─ {advice['reason']}")
            
            # 链接
            report_lines.append("")
            purchase_link = price_info.get('purchase_link') if price_info else deal['link']
            manmanbuy_link = price_info.get('manmanbuy_link') if price_info else None
            source = price_info.get('source') if price_info else '什么值得买'
            
            report_lines.append(f"🛒 购买链接: <{purchase_link}>")
            if manmanbuy_link:
                report_lines.append(f"📊 查看历史价格: <{manmanbuy_link}>")
        
        # 添加总结
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("📊 **今日统计**:")
        report_lines.append(f"• ✅ 建议入手: {buy_now_count} 个")
        report_lines.append(f"• ⏰ 建议等待: {wait_count} 个")
        report_lines.append("")
        report_lines.append("⚠️ 提醒:")
        report_lines.append("• 价格实时变化，建议尽快查看")
        report_lines.append("• 历史价格仅供参考，以实际为准")
        report_lines.append("• 部分优惠需用券或有地区限制")
        report_lines.append("")
        report_lines.append("📅 下次更新: 9:00 AM / 12:00 PM / 6:00 PM")
        
        # 保存已发送记录
        for deal in top_deals:
            deal_key = deal['title'][:50]
            sent_deals[deal_key] = now.isoformat()
        
        self.save_sent_deals(sent_deals)
        
        return "\n".join(report_lines)

def main():
    print("🐑 deals-hunter v6.0")
    print("=" * 60)
    
    hunter = DealsHunter()
    
    # 获取数据
    hunter.fetch_smzdm_rss()
    
    # 生成报告
    report = hunter.generate_detailed_report()
    
    if report:
        print("\n" + "=" * 60)
        print("📄 报告生成完成！")
        print("=" * 60)
        print(report)
        
        # 保存报告
        report_file = '/Users/xufan65/.openclaw/workspace/memory/deals-report-latest.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 报告已保存到: {report_file}")
    else:
        print("\n⚠️  没有生成报告")

if __name__ == "__main__":
    main()
