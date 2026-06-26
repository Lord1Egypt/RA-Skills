---
name: china-commodity-quotes
description: Query real-time Chinese commodity futures, financial index futures, crude oil, and shipping index prices across all exchanges.
emoji: 📊
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: SINARA_REFERER
        required: false
        description: Custom referer for Sina Finance API (defaults to https://finance.sina.com.cn)
---

# China Futures Quotes — 中国期货行情查询

Real-time futures prices across all Chinese exchanges: commodity futures (郑商所/大商所/上期所/广期所), financial index futures (中金所), crude oil & shipping (国际能源中心).

## Exchange & Contract Reference

### 中金所 CFFEX — Financial Index Futures (金融股指期货)

| Product | Contract Prefix | Tick Size | Contract Multiplier |
|:--------|:----------------|:----------|:--------------------|
| 沪深300股指 IF | IF | 0.2 pt | ¥300/pt |
| 上证50股指 IH | IH | 0.2 pt | ¥300/pt |
| 中证500股指 IC | IC | 0.2 pt | ¥200/pt |
| 中证1000股指 IM | IM | 0.2 pt | ¥200/pt |
| 10年期国债 T | T | 0.005 pt | ¥10,000/pt |
| 5年期国债 TF | TF | 0.005 pt | ¥10,000/pt |
| 2年期国债 TS | TS | 0.005 pt | ¥20,000/pt |
| 30年期国债 TL | TL | 0.005 pt | ¥10,000/pt |

### 上期所 SHFE — Metals, Rubber, etc.

| Product | Prefix | Product | Prefix |
|:--------|:-------|:--------|:-------|
| 铜 CU | CU | 铝 AL | AL |
| 锌 ZN | ZN | 铅 PB | PB |
| 镍 NI | NI | 锡 SN | SN |
| 黄金 AU | AU | 白银 AG | AG |
| 螺纹钢 RB | RB | 线材 WR | WR |
| 热卷 HC | HC | 不锈钢 SS | SS |
| 橡胶 RU | RU | 沥青 BU | BU |
| 燃料油 FU | FU | 纸浆 SP | SP |
| 丁二烯橡胶 BR | BR | 氧化铝 AO | AO |

### 大商所 DCE — Agricultural, Ferrous, Chemical

| Product | Prefix | Product | Prefix |
|:--------|:-------|:--------|:-------|
| 铁矿石 I | I | 焦煤 JM | JM |
| 焦炭 J | J | 玉米 C | C |
| 玉米淀粉 CS | CS | 豆一 A | A |
| 豆二 B | B | 豆粕 M | M |
| 豆油 Y | Y | 棕榈油 P | P |
| 塑料 L | L | 聚丙烯 PP | PP |
| PVC V | V | 乙二醇 EG | EG |
| 苯乙烯 EB | EB | 液化气 PG | PG |
| 生猪 LH | LH | 鸡蛋 JD | JD |
| 粳米 RR | RR | 原木 LG | LG |

### 郑商所 ZCE — Agricultural, Chemical, Energy

| Product | Prefix | Product | Prefix |
|:--------|:-------|:--------|:-------|
| 棉花 CF | CF | 白糖 SR | SR |
| 锰硅 SM | SM | 硅铁 SF | SF |
| 尿素 UR | UR | 纯碱 SA | SA |
| 对二甲苯 PX | PX | PTA TA | TA |
| 甲醇 MA | MA | 短纤 PF | PF |
| 菜粕 RM | RM | 菜油 OI | OI |
| 玻璃 FG | FG | 苹果 AP | AP |
| 红枣 CJ | CJ | 花生 PK | PK |
| 烧碱 SH | SH | 动力煤 ZC | ZC (paused) |

### 广期所 GFEX

| Product | Prefix |
|:--------|:-------|
| 工业硅 SI | SI |
| 多晶硅 PS | PS |
| 碳酸锂 LC | LC |

### 国际能源中心 INE

| Product | Prefix |
|:--------|:-------|
| 原油 SC | SC |
| 低硫燃料油 LU | LU |
| 20号胶 NR | NR |
| 国际铜 BC | BC |
| **集运欧线 EC** | **EC** |

## How to Use

### Step 1: Identify the contract code

Format: `<Prefix><YYMM>` (e.g., `IF2606` = 沪深300, 2026年6月合约)

**Common contract codes:**
- 沪深300股指期货: IF2606
- 中证500股指期货: IC2609
- 中证1000股指: IM2609
- 上证50股指: IH2606
- 原油: SC2609
- **集运欧线: EC2608** (主力合约)
- 铜: CU2609
- 螺纹钢: RB2610
- 铁矿石: I2609
- 棉花: CF2609
- 白糖: SR2609
- 纯碱: SA2609

**Continuous contracts (quick snapshot):** Append "0" after prefix — e.g., IF0, SC0, EC0, CF0, I0

### Step 2: Fetch data

**Method A: Browser Snapshot (Recommended — full real-time data)**
1. Navigate to `https://finance.sina.com.cn/futures/quotes/<CODE>.shtml`
2. Wait ~2s for page to fully render
3. Take a snapshot (compact mode)
4. Extract from the contract-specific section: 最新价(price), 开盘价(open), 最高价(high), 最低价(low), 昨结算(prev settlement), 持仓量(OI), 成交量(volume), 涨跌幅(change%)

**Example: 沪深300股指**
```
Navigate → https://finance.sina.com.cn/futures/quotes/IF2606.shtml
Snapshot → look for price data rows
```

**Example: 集运欧线**
```
Navigate → https://finance.sina.com.cn/futures/quotes/EC2608.shtml
Snapshot → look for price data rows
```

**Method B: curl Continuous Contract (Quick)**
```bash
curl -s -e "https://finance.sina.com.cn" "https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,SC0,EC0"
```
Response: `var hq_str_XX0="name,ts,prev_close,open,current,high,low,...,volume,OI,..."`
Key fields: index 2=prev_close, 3=open, 4=current, 5=high, 6=low, 12=volume, 13=OI

### Step 3: Format output

Present as a clean breakdown:
```
📊 [品种] [合约] 实时行情 (时间)
🟢/🔴 最新: XXXXX  涨跌幅: +X.XX%
  开盘: XXXXX     最高: XXXXX
  最低: XXXXX     昨结算: XXXXX
  持仓量: XXX    成交量: XXX
```

Across multiple contracts, use a compact table:
```
📊 期货组合行情
品种      合约    最新价   涨跌幅
IF沪深300  IF2606  XXXX   +X.XX% 🟢
IC中证500  IC2609  XXXX   -X.XX% 🔴
SC原油     SC2609  XXX    +X.XX% 🟢
EC集运     EC2608  XXXX   -X.XX% 🔴
```

## Trading Hours

| Session | Time (GMT+8) | Markets |
|:--------|:-------------|:--------|
| Morning | 09:00-10:15, 10:30-11:30 | All |
| Afternoon | 13:30-15:00 | All |
| Night | 21:00-23:00 | Most commodities (not financial futures/EC) |
| Night | 21:00-02:30 | 原油 SC, 黄金 AU, 白银 AG |

Note: 金融股指期货 IF/IC/IH/IM and 集运 EC have NO night session (只做日盘).

## Special Notes

- **集运欧线 EC** trades 09:00-10:15, 10:30-11:30, 13:30-15:00 (日盘 only, no夜盘)
- **原油 SC** 夜盘到次日02:30
- Financial index futures (IF/IC/IH/IM) settle in cash, no physical delivery
- The Sina API requires a proper Referer header when called via direct curl
- Use `web_fetch` with Sina page URLs as a fallback (gets basic info, price data is JS-rendered)
