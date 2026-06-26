import datetime

class PlumBlossomEngine:
    """梅花易数算法引擎"""
    def __init__(self):
        pass

    def calculate(self, year=None, month=None, day=None, hour=None):
        now = datetime.datetime.now()
        year = year or now.year
        month = month or now.month
        day = day or now.day
        hour = hour or now.hour
        
        # 地支数处理
        year_zhi = (year - 4) % 12 + 1
        
        upper = (year_zhi + month + day) % 8
        upper = 8 if upper == 0 else upper
        
        lower = (year_zhi + month + day + hour) % 8
        lower = 8 if lower == 0 else lower
        
        yao = (year_zhi + month + day + hour) % 6
        yao = 6 if yao == 0 else yao
        
        return {
            "upper": upper,
            "lower": lower,
            "yao": yao
        }
