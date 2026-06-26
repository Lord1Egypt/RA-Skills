import datetime

def get_gua_numbers(year=None, month=None, day=None, hour=None):
    """梅花易数起卦算法"""
    now = datetime.datetime.now()
    year = year or now.year
    month = month or now.month
    day = day or now.day
    hour = hour or now.hour
    
    # 简易地支数处理 (1-12)
    year_zhi = (year - 4) % 12 + 1
    
    upper = (year_zhi + month + day) % 8
    upper = 8 if upper == 0 else upper
    
    lower = (year_zhi + month + day + hour) % 8
    lower = 8 if lower == 0 else lower
    
    yao = (year_zhi + month + day + hour) % 6
    yao = 6 if yao == 0 else yao
    
    return upper, lower, yao

if __name__ == "__main__":
    u, l, y = get_gua_numbers()
    print(f"上卦: {u}, 下卦: {l}, 变爻: {y}")
