# 过滤规则 V4

## 大品牌（自动过滤，不可跟卖/侵权风险）

ASICS, DJI, adidas, Anker, Soundcore, OLIGHT, Plaud, Nike, Apple, Samsung, Sony, Bose, Dyson, iRobot, Ninja, KitchenAid, Vitamix, Lego, Nintendo, Patagonia, North Face, Under Armour, New Balance, Puma, Reebok, Converse, Vans, Columbia, NOCO, Autel, Tesla, WeatherTech, Thule, Yakima, K&N, PowerStop, Borla, MagnaFlow, Extang, BAK, Garmin, Nextbase

## 高退货率品类（退货率>15%）

关键词匹配（title不区分大小写）：
shoe, running shoe, sneaker, boot, sandal, slipper,
dress, clothing, apparel, shirt, pant, skirt, blouse, jacket, coat, sweater, hoodie,
bra, underwear, lingerie, swimsuit, bikini

## 自动HIGH IP风险品类

以下品类自动标记🔴HIGH并淘汰：
- tri-fold tonneau cover (Extang/BAK专利)
- jump starter (NOCO外观专利)
- diagnostic tool, OBD scanner (Autel/LAUNCH授权制)
- wireless carplay screen (Apple MFi)
- OEM grille replica

## 过滤逻辑

```python
BIG_BRANDS = {'ASICS','DJI','adidas','Anker','Nike','Apple','Samsung','Sony',
              'Bose','Dyson','NOCO','Autel','Tesla','WeatherTech','Thule',
              'K&N','PowerStop','Borla','MagnaFlow','Extang','BAK','Garmin'}

HIGH_RETURN_KW = ['shoe','running','dress','clothing','apparel','shirt',
                  'pant','skirt','jacket','coat','sweater','boot','sandal',
                  'sneaker','bra','underwear','swimsuit']

AUTO_HIGH_IP = ['tonneau cover','jump starter','diagnostic tool',
                'obd scanner','carplay screen','oem grille']

def should_filter(product):
    if product['brand'] in BIG_BRANDS:
        return True, 'big_brand'
    title_lower = product['title'].lower()
    if any(kw.lower() in title_lower for kw in HIGH_RETURN_KW):
        return True, 'high_return'
    if any(kw in title_lower for kw in AUTO_HIGH_IP):
        return True, 'high_ip_risk'
    return False, 'pass'
```
