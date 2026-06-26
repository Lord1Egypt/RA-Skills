import akshare as ak
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def scan_bonds():
    print("⏳ 正在扫描全市场可转债底牌...")
    try:
        df = ak.bond_zh_hs_cov_spot()
        df['转股溢价率'] = pd.to_numeric(df['转股溢价率'], errors='coerce')
        df['最新价'] = pd.to_numeric(df['最新价'], errors='coerce')
        
        # 游资审美过滤逻辑：
        # 1. 价格不能太高（>130通常透支了弹性，100-130之间最安全且有爆发力）
        # 2. 按转股溢价率从低到高排序
        target_bonds = df[(df['最新价'] <= 130) & (df['最新价'] >= 100)]
        top_bonds = target_bonds.sort_values(by='转股溢价率').head(10)
        
        print("\n🔥 [游资雷达] 现价 100-130元 内，转股溢价率最低的 Top 10 埋伏标的：")
        print(top_bonds[['代码', '名称', '最新价', '转股溢价率', '正股名称', '正股最新价']].to_string(index=False))
    except Exception as e:
        print(f"转债扫描失败: {e}")

def scan_cross_etfs():
    print("\n⏳ 正在扫描全市场跨境 ETF 资金热度...")
    try:
        df = ak.fund_etf_spot_em()
        
        # 锁定跨境关键词
        keywords = ['纳指', '标普', '日经', '沙特', '恒生', '黄金']
        df_cross = df[df['名称'].str.contains('|'.join(keywords), na=False)]
        
        # 游资审美过滤逻辑：
        # ETF不看价格，看“换手率”（代表资金活跃度和流动性），按换手率降序
        df_cross['换手率'] = pd.to_numeric(df_cross['换手率'], errors='coerce')
        top_etfs = df_cross.sort_values(by='换手率', ascending=False).head(5)
        
        print("\n⚠️ [游资雷达] 当前资金最活跃（换手率最高）的跨境 ETF Top 5：")
        print(top_etfs[['代码', '名称', '最新价', '涨跌幅', '换手率', '成交额']].to_string(index=False))
    except Exception as e:
        print(f"ETF扫描失败: {e}")

if __name__ == "__main__":
    print("=============================================")
    print("      ⚔️ 悟空老板的专属游资盘前雷达 ⚔️")
    print("=============================================\n")
    scan_bonds()
    scan_cross_etfs()
    print("\n=============================================")
