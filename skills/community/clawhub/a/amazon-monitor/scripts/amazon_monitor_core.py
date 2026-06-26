"""
Amazon商品数据采集核心模块
功能：抓取商品标题、价格、星级、评论数
"""
import asyncio
import json
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

def get_product_data(asin, zip_code="10001"):
    """
    获取Amazon商品数据
    """
    async def _scrape():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                locale='en-US',
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9'
                }
            )
            page = await context.new_page()
            
            await page.goto(f'https://www.amazon.com/dp/{asin}', 
                            wait_until='domcontentloaded', timeout=120000)
            await asyncio.sleep(5)
            
            # 设置邮编
            if zip_code:
                try:
                    location_btn = await page.query_selector('#glow-ingress-line2')
                    if location_btn:
                        await location_btn.click()
                        await asyncio.sleep(3)
                    
                    zip_input = await page.query_selector('#GLUXZipUpdateInput')
                    if zip_input:
                        await zip_input.fill(zip_code)
                        await asyncio.sleep(1)
                        
                        submit_btn = await page.query_selector('#GLUXZipUpdate')
                        if submit_btn:
                            await submit_btn.click()
                            await asyncio.sleep(8)
                except:
                    pass
                
                await page.reload(wait_until='domcontentloaded')
                await asyncio.sleep(5)
            
            # 检查页面是否有效
            page_title = await page.title()
            if 'Page Not Found' in page_title or '找不到' in page_title:
                await browser.close()
                return {
                    'asin': asin,
                    'valid': False,
                    'error': '链接失效或页面不存在'
                }
            
            # 获取商品名称
            title_el = await page.query_selector('#productTitle')
            name = await title_el.inner_text() if title_el else '未找到'
            
            if name and len(name) < 50:
                page_title_str = await page.title()
                if page_title_str:
                    full_name = page_title_str.split(' : ')[0] if ' : ' in page_title_str else page_title_str
                    if len(full_name) > len(name):
                        name = full_name
            
            # 获取价格
            price_el = await page.query_selector('.a-price .a-offscreen')
            price = await price_el.inner_text() if price_el else '未找到'
            
            # 获取星级
            rating_el = await page.query_selector('#acrPopover .a-icon-alt')
            rating = await rating_el.inner_text() if rating_el else '未找到'
            
            # 获取评论数
            reviews_el = await page.query_selector('#acrCustomerReviewText')
            reviews = await reviews_el.inner_text() if reviews_el else '未找到'
            
            # 获取配送地址
            location_text = await page.query_selector('#glow-ingress-line2')
            location = await location_text.inner_text() if location_text else ''
            location_clean = re.sub(r'[^\x00-\x7F]', '', location)
            
            await browser.close()
            
            return {
                'asin': asin,
                'productName': name.strip(),
                'price': price,
                'rating': rating,
                'reviewCount': reviews,
                'location': location_clean,
                'parseTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'valid': True
            }
    
    return asyncio.run(_scrape())


def save_history(asin, data, zip_code="10001"):
    """保存历史数据"""
    json_file = f"{asin}_history.json"
    
    entry = {
        'asin': asin,
        'productName': data.get('productName', ''),
        'price': data.get('price', ''),
        'rating': data.get('rating', ''),
        'reviewCount': data.get('reviewCount', ''),
        'zipCode': zip_code,
        'parseTime': data.get('parseTime', '')
    }
    
    history = []
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    history.append(entry)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return history


def generate_trend_chart(asin, history):
    """生成趋势图"""
    if len(history) < 2:
        return None
    
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    
    def extract_price(p):
        match = re.search(r'[\d,.]+', str(p))
        if not match:
            return 0
        val = match.group().replace(',', '')
        while '..' in val:
            val = val.replace('..', '.')
        try:
            return float(val)
        except:
            return 0
    
    def extract_reviews(r):
        match = re.search(r'[\d,]+', str(r))
        return int(match.group().replace(',', '')) if match else 0
    
    def extract_rating(r):
        match = re.search(r'[\d.]+', str(r))
        return float(match.group()) if match else 0
    
    times = [d['parseTime'] for d in history]
    prices = [extract_price(d['price']) for d in history]
    reviews_list = [extract_reviews(d['reviewCount']) for d in history]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 价格趋势
    ax1.plot(times, prices, marker='o', color='#E35F21', linewidth=2, markersize=8)
    ax1.set_title(f'Price Trend (ASIN: {asin})', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    for i, (t, pr) in enumerate(zip(times, prices)):
        ax1.annotate(f'${pr:.2f}', (t, pr), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9)
    
    # 评论趋势
    ax2.plot(times, reviews_list, marker='s', color='#2E86AB', linewidth=2, markersize=8)
    ax2.set_title('Review Count Trend', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Review Count', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    for i, (t, rv) in enumerate(zip(times, reviews_list)):
        ax2.annotate(f'{rv:,}', (t, rv), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9)
    
    plt.tight_layout()
    chart_file = f'{asin}_trend_chart.png'
    plt.savefig(chart_file, dpi=150, bbox_inches='tight')
    
    return chart_file


def check_trigger_conditions(current_data, previous_data):
    """
    检查触发条件
    返回: {条件名: (是否触发, 变化描述)}
    """
    results = {}
    
    if not previous_data:
        return results
    
    # 价格变化
    def extract_price(p):
        match = re.search(r'[\d,.]+', str(p))
        if not match:
            return 0
        return float(match.group().replace(',', ''))
    
    # 评论数变化
    def extract_reviews(r):
        match = re.search(r'[\d,]+', str(r))
        return int(match.group().replace(',', '')) if match else 0
    
    # 星级变化
    def extract_rating(r):
        match = re.search(r'[\d.]+', str(r))
        return float(match.group()) if match else 0
    
    curr_price = extract_price(current_data.get('price', ''))
    prev_price = extract_price(previous_data.get('price', ''))
    
    if curr_price != prev_price and prev_price > 0:
        change_pct = ((curr_price - prev_price) / prev_price) * 100
        results['price_change'] = (True, f'价格从${prev_price:.2f}变为${curr_price:.2f} ({change_pct:+.1f}%)')
    else:
        results['price_change'] = (False, f'价格稳定: ${curr_price:.2f}')
    
    curr_reviews = extract_reviews(current_data.get('reviewCount', ''))
    prev_reviews = extract_reviews(previous_data.get('reviewCount', ''))
    
    if curr_reviews != prev_reviews:
        results['review_change'] = (True, f'评论数从{prev_reviews}变为{curr_reviews} ({curr_reviews - prev_reviews:+,}条)')
    else:
        results['review_change'] = (False, f'评论数稳定: {curr_reviews}')
    
    curr_rating = extract_rating(current_data.get('rating', ''))
    prev_rating = extract_rating(previous_data.get('rating', ''))
    
    if curr_rating != prev_rating and prev_rating > 0:
        results['rating_change'] = (True, f'星级从{prev_rating}变为{curr_rating}')
    else:
        results['rating_change'] = (False, f'星级稳定: {curr_rating}/5')
    
    # 链接有效性
    results['link_valid'] = (current_data.get('valid', True), '链接有效' if current_data.get('valid', True) else '链接失效!')
    
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python amazon_monitor_core.py <ASIN> [ZIP_CODE]")
        sys.exit(1)
    
    asin = sys.argv[1]
    zip_code = sys.argv[2] if len(sys.argv) > 2 else "10001"
    
    print(f"正在采集 ASIN: {asin}, 邮编: {zip_code}")
    data = get_product_data(asin, zip_code)
    
    if data.get('valid', True):
        print(f"商品名称: {data.get('productName', '')[:60]}...")
        print(f"价格: {data.get('price')}")
        print(f"星级: {data.get('rating')}")
        print(f"评论数: {data.get('reviewCount')}")
        print(f"配送地址: {data.get('location')}")
        
        history = save_history(asin, data, zip_code)
        print(f"历史记录已保存，共 {len(history)} 条")
        
        if len(history) >= 2:
            chart_file = generate_trend_chart(asin, history)
            if chart_file:
                print(f"趋势图已生成: {chart_file}")
    else:
        print(f"错误: {data.get('error', '未知错误')}")
