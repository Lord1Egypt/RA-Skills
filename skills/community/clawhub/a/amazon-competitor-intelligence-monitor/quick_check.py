import json
import subprocess
import os
import datetime

DIR = "/Users/gutingyi/.openclaw/workspace/projects/apiclaw/APIClaw-Skills/amazon-competitor-intelligence-monitor/"
DATA_DIR = os.path.join(DIR, "monitor-data")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
BASELINE_PATH = os.path.join(DATA_DIR, "baseline.json")

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_apiclaw(asin):
    cmd = ["python3", os.path.join(DIR, "scripts/apiclaw.py"), "product", "--asin", asin]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except:
        return None

def main():
    config = load_json(CONFIG_PATH)
    os.environ['APICLAW_API_KEY'] = config['api_key']
    baseline = load_json(BASELINE_PATH)
    
    asins = config['tracked_asins']
    labels = config.get('asin_labels', {})
    price_thr = config['alert_thresholds']['price_change_pct']
    bsr_thr = config['alert_thresholds']['bsr_change_pct']
    
    new_snapshot = {
        "timestamp": datetime.datetime.now().isoformat(),
        "asins": {}
    }
    
    red_alerts = []
    yellow_alerts = []
    
    for asin in asins:
        label = labels.get(asin, asin)
        data_full = run_apiclaw(asin)
        if not data_full or not data_full.get('success'):
            continue
            
        data = data_full['data']
        try:
            price = data.get('buyboxWinner', {}).get('price', {}).get('value', 0)
            rating = data.get('rating', 0)
            ratingCount = data.get('ratingCount', 0)
            
            ranks = data.get('bestsellersRank', [])
            bsr_pet = ranks[0]['rank'] if len(ranks)>0 else 0
            bsr_sub = ranks[1]['rank'] if len(ranks)>1 else 0
            subcat = ranks[1]['category'] if len(ranks)>1 else ""
            
            bb_seller = data.get('buyboxWinner', {}).get('fulfillment', {}).get('soldBy', '')
            title = data.get('title', '')
            
            new_data = {
                "price": price,
                "rating": rating,
                "ratingCount": ratingCount,
                "bsr_pet": bsr_pet,
                "bsr_sub": bsr_sub,
                "subcat": subcat,
                "buyboxSeller": bb_seller,
                "title": title
            }
            new_snapshot['asins'][asin] = new_data
            
            base_data = baseline['asins'].get(asin, {})
            if not base_data:
                continue
                
            # Compare
            # Price
            old_price = base_data.get('price', price)
            if old_price is not None and old_price > 0 and price is not None:
                price_diff_pct = abs(price - old_price) / old_price * 100
                if price_diff_pct > price_thr:
                    red_alerts.append(f"🔴 [{label}] 价格变动 >{price_thr}%: ${old_price} -> ${price}")
            
            # BSR
            old_bsr = base_data.get('bsr_pet', bsr_pet)
            if old_bsr is not None and old_bsr > 0 and bsr_pet is not None:
                bsr_diff_pct = abs(bsr_pet - old_bsr) / old_bsr * 100
                if bsr_diff_pct > bsr_thr:
                    red_alerts.append(f"🔴 [{label}] 大类BSR变动 >{bsr_thr}%: #{old_bsr} -> #{bsr_pet}")
                    
            # BuyBox
            old_bb = base_data.get('buyboxSeller', bb_seller)
            if old_bb != bb_seller:
                red_alerts.append(f"🔴 [{label}] Buy Box 易主: {old_bb} -> {bb_seller}")
                
            # Rating / Reviews
            old_rating = base_data.get('rating', rating)
            if old_rating != rating:
                yellow_alerts.append(f"🟡 [{label}] 评分变化: {old_rating} -> {rating}")
                
            old_rc = base_data.get('ratingCount', ratingCount)
            if old_rc is not None and ratingCount is not None and ratingCount - old_rc > 10:
                yellow_alerts.append(f"🟡 [{label}] 评论数快速增长: {old_rc} -> {ratingCount}")
                
            # Title
            old_title = base_data.get('title', title)
            if old_title != title:
                yellow_alerts.append(f"🟡 [{label}] 标题(Listing)修改")
                
        except Exception as e:
            pass

    # Save history
    hist_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    save_json(os.path.join(DATA_DIR, "history", hist_name), new_snapshot)
    
    # Update baseline
    save_json(BASELINE_PATH, new_snapshot)
    
    if red_alerts:
        print("发现重要变动 (🔴 告警):")
        print("\n".join(red_alerts))
        if yellow_alerts:
            print("\n其他变动 (🟡 摘要):")
            print("\n".join(yellow_alerts))
    else:
        print("一切正常")

if __name__ == "__main__":
    main()
