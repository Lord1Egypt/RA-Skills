import akshare as ak
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime, timedelta
import os
import io
from typing import Dict, List, Tuple, Optional, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class Config:
    """Configuration class for the All Weather Strategy."""
    
    # Global Plotting Configuration
    PLT_PARAMS = {
        "font.family": ["SimHei", "Microsoft YaHei", "sans-serif"],
        "axes.unicode_minus": False,
        "figure.dpi": 120,
        "font.size": 11
    }
    
    # Pandas display configurations
    PD_OPTIONS = {
        'display.unicode.ambiguous_as_wide': True,
        'display.unicode.east_asian_width': True,
        'display.width': 140
    }
    
    DEFAULT_ETF_LIST = ["159201", "588290", "159531", "159545", "515450", "513100", "518880"]
    DEFAULT_AMOUNT = 10000.0
    DEFAULT_LOOKBACK = 365
    OUTPUT_DIR = "全天候配置报告"
    COPYRIGHT = "Copyright © 2026 wzwangyc. All Rights Reserved."
    AUTHOR = "wzwangyc"
    
    @classmethod
    def apply_settings(cls):
        """Apply the configuration settings to the environment."""
        for key, value in cls.PLT_PARAMS.items():
            plt.rcParams[key] = value
        for key, value in cls.PD_OPTIONS.items():
            pd.set_option(key, value)

    @staticmethod
    def register_chinese_font() -> str:
        """Register a Chinese font for PDF generation."""
        font_name = "SimHei"
        try:
            pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))
            return "SimHei"
        except:
            font_candidates = [
                ("MicrosoftYaHei", "msyh.ttc"),
                ("PingFang", "/System/Library/Fonts/PingFang.ttc"),
                ("WenQuanYiMicroHei", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
            ]
            for fn, fp in font_candidates:
                if os.path.exists(fp):
                    try:
                        pdfmetrics.registerFont(TTFont(fn, fp))
                        return fn
                    except:
                        continue
            return "Helvetica"

class DataFetcher:
    """Handles data retrieval for ETFs from multiple sources."""
    
    @staticmethod
    def get_yf_symbol(symbol: str) -> str:
        """Transform ETF symbol to yfinance format."""
        if not symbol.isdigit():
            return symbol
        first_digit = symbol[0]
        if first_digit == '5':
            return f"{symbol}.SS"
        elif first_digit in ['1', '3']:
            return f"{symbol}.SZ"
        return symbol

    def get_etf_data(self, symbol: str, start_date: str, end_date: str) -> Tuple[Optional[pd.Series], Optional[float]]:
        """Retrieve ETF historical returns and latest price."""
        ak_start = start_date.replace("-", "")
        ak_end = end_date.replace("-", "")
        
        # Try AkShare
        try:
            df = ak.fund_etf_hist_em(
                symbol=symbol, period="daily", start_date=ak_start, end_date=ak_end, adjust="qfq"
            )
            df['日期'] = pd.to_datetime(df['日期'])
            df = df.set_index('日期').sort_index()
            df['涨跌幅'] = df['收盘'].pct_change()
            df = df.dropna()
            if not df.empty:
                return df['涨跌幅'], df.iloc[-1]['收盘']
        except:
            pass
        
        # Try yfinance
        try:
            yf_symbol = self.get_yf_symbol(symbol)
            df = yf.download(
                tickers=yf_symbol, start=start_date, end=end_date, auto_adjust=True, progress=False
            )
            df['涨跌幅'] = df['Close'].pct_change()
            df = df.dropna()
            if not df.empty:
                close_data = df.iloc[-1]['Close']
                latest_price = close_data.item() if isinstance(close_data, pd.Series) else close_data
                return df['涨跌幅'], float(latest_price)
        except:
            pass
            
        return None, None

    def get_etf_name(self, symbol: str) -> str:
        """Get the descriptive name of an ETF."""
        try:
            fund_df = ak.fund_exchange_rank_em()
            match_df = fund_df[fund_df['基金代码'] == symbol]
            if not match_df.empty:
                return match_df['基金简称'].iloc[0]
        except:
            pass
            
        try:
            yf_symbol = self.get_yf_symbol(symbol)
            ticker = yf.Ticker(yf_symbol)
            yf_name = ticker.info.get('longName', ticker.info.get('shortName', f"ETF({symbol})"))
            return yf_name[:20] + "..." if len(yf_name) > 20 else yf_name
        except:
            pass
            
        return f"ETF({symbol})"

class RiskParityStrategy:
    """Calculates asset allocation weights and portfolio metrics."""
    
    def calculate_weights(self, returns_df: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        """Perform risk parity optimization."""
        cov_matrix = returns_df.cov() * 252
        n = len(returns_df.columns)
        
        def risk_contribution(weights):
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            marginal_risk = np.dot(cov_matrix, weights) / portfolio_vol
            return weights * marginal_risk

        def objective(weights):
            rc = risk_contribution(weights)
            return np.sum((rc - np.mean(rc)) ** 2)

        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(n))
        initial_weights = np.array([1 / n] * n)

        solution = minimize(
            objective, initial_weights, method='SLSQP',
            constraints=constraints, bounds=bounds,
            tol=1e-12, options={'maxiter': 5000, 'ftol': 1e-12, 'disp': False}
        )
        return solution.x, cov_matrix

    def calculate_metrics(self, weights: np.ndarray, returns_df: pd.DataFrame, cov_matrix: pd.DataFrame) -> Dict[str, float]:
        """Calculate annualized return and risk for the portfolio."""
        annual_returns = returns_df.mean() * 252
        portfolio_return = np.dot(weights, annual_returns)
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        return {
            "annualized_return": float(portfolio_return),
            "annualized_risk": float(portfolio_vol)
        }

class ReportGenerator:
    """Handles generation of CSV and PDF reports."""
    
    def __init__(self, font_name: str, total_amount: float):
        self.font_name = font_name
        self.total_amount = total_amount
        self.styles = getSampleStyleSheet()

    @staticmethod
    def wrap_text(text: str, max_len: int = 10) -> str:
        """Wrap text for better display in charts."""
        if len(text) <= max_len:
            return text
        return '\n'.join([text[i:i+max_len] for i in range(0, len(text), max_len)])

    def generate_csv(self, df: pd.DataFrame, path: str):
        """Export result dataframe to CSV."""
        df.to_csv(path, index=False, encoding='utf-8-sig')

    def generate_pdf(self, result_df: pd.DataFrame, weights: np.ndarray, etf_names: Dict[str, str], output_path: str):
        """Generate a visual PDF report with table and pie chart."""
        doc = SimpleDocTemplate(
            output_path, pagesize=A4, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2
        )
        story = []
        
        title_style = ParagraphStyle('CustomTitle', parent=self.styles['Title'], fontName=self.font_name, fontSize=18, alignment=1)
        story.append(Paragraph(f"ETF全天候配置报告", title_style))
        story.append(Paragraph(f"（总金额：{self.total_amount:.2f}元）", ParagraphStyle('Sub', parent=title_style, fontSize=12)))
        story.append(Spacer(1, 12))
        
        # Copyright at top
        copy_style = ParagraphStyle('Copyright', parent=self.styles['Normal'], fontName=self.font_name, fontSize=8, alignment=1, textColor=colors.grey)
        story.append(Paragraph(Config.COPYRIGHT, copy_style))
        story.append(Spacer(1, 12))
        
        h2_style = ParagraphStyle('CustomHeading2', parent=self.styles['Heading2'], fontName=self.font_name, fontSize=12, spaceAfter=10)
        
        table_data = [result_df.columns.tolist()] + result_df.values.tolist()
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(Paragraph("配置方案详情", h2_style))
        story.append(table)
        story.append(Spacer(1, 20))
        
        self._add_pie_chart(story, result_df, weights, etf_names, h2_style)
        
        doc.build(story)

    def _add_pie_chart(self, story: List, result_df: pd.DataFrame, weights: np.ndarray, etf_names: Dict[str, str], h2_style: ParagraphStyle):
        """Internal method to create and add pie chart to PDF story."""
        sorted_pairs = sorted(zip(weights, [self.wrap_text(f"{etf_names[code]}({code})") for code in result_df['ETF代码']]), key=lambda x: x[0], reverse=True)
        sorted_weights = [p[0] for p in sorted_pairs]
        sorted_labels = [p[1] for p in sorted_pairs]
        
        fig = self.create_pie_chart(sorted_weights, sorted_labels)
        
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img = Image(img_buffer, width=6*inch, height=4*inch)
        plt.close(fig)
        
        story.append(Paragraph("权重分布可视化", h2_style))
        story.append(img)

    def create_pie_chart(self, weights, labels):
        """Create and return a matplotlib figure for the pie chart."""
        fig = plt.figure(figsize=(10, 7))
        explode = [0.05] * len(labels)
        plt.pie(
            weights, labels=labels, autopct='%1.1f%%',
            startangle=90, explode=explode, textprops={'fontsize': 10},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        plt.title(f'ETF配置权重分布（总金额：{self.total_amount:.2f}元）', fontsize=14, pad=25)
        plt.axis('equal')
        plt.tight_layout()
        return fig

class AllWeatherEngine:
    """The main engine orchestrating the strategy execution."""
    
    def __init__(self, etf_symbols: List[str]):
        Config.apply_settings()
        self.etf_symbols = etf_symbols
        self.fetcher = DataFetcher()
        self.strategy = RiskParityStrategy()
        
    def run(self, total_amount: float, lookback_days: int = 365, progress_callback=None):
        """Execute the full workflow."""
        if progress_callback: progress_callback(0.1, "正在初始化数据获取...")
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        
        all_returns = {}
        latest_prices = {}
        etf_names = {}
        
        num_etfs = len(self.etf_symbols)
        for i, symbol in enumerate(self.etf_symbols):
            if progress_callback:
                progress_callback(0.2 + (i / num_etfs) * 0.5, f"正在获取 {symbol} 数据...")
                
            name = self.fetcher.get_etf_name(symbol)
            etf_names[symbol] = name
            returns, price = self.fetcher.get_etf_data(symbol, start_date, end_date)
            if returns is not None and price is not None:
                all_returns[symbol] = returns
                latest_prices[symbol] = price
            else:
                print(f"警告: 无法获取 {name}({symbol}) 的数据")

        if not all_returns:
            if progress_callback: progress_callback(1.0, "错误: 所有ETF数据获取失败")
            return None
        
        if progress_callback: progress_callback(0.8, "正在计算风险平配权重...")
        
        returns_df = pd.DataFrame(all_returns).dropna()
        weights, cov_matrix = self.strategy.calculate_weights(returns_df)
        metrics = self.strategy.calculate_metrics(weights, returns_df, cov_matrix)

        result_data = []
        for i, symbol in enumerate(returns_df.columns):
            weight = weights[i]
            alloc_amount = total_amount * weight
            price = latest_prices[symbol]
            shares = int((alloc_amount // price) // 100 * 100)
            actual_amount = shares * price

            result_data.append({
                'ETF代码': symbol,
                'ETF名称': etf_names[symbol],
                '权重': f"{weight * 100:.2f}%",
                '配置金额(元)': round(alloc_amount, 2),
                '最新价格(元)': round(price, 3),
                '可购股数(股)': shares,
                '实际投入金额(元)': round(actual_amount, 2)
            })

        result_df = pd.DataFrame(result_data).sort_values(
            '权重', 
            key=lambda x: x.str.strip('%').astype(float), 
            ascending=False
        ).reset_index(drop=True)
        
        if progress_callback: progress_callback(1.0, "配置完成！")
        
        return {
            "result_df": result_df,
            "weights": weights,
            "etf_names": etf_names,
            "metrics": metrics
        }

    def save_reports(self, result_df: pd.DataFrame, weights: np.ndarray, etf_names: Dict[str, str], total_amount: float):
        """CLI helper to save report files."""
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d')
        font_name = Config.register_chinese_font()
        generator = ReportGenerator(font_name, total_amount)
        
        csv_path = os.path.join(Config.OUTPUT_DIR, f"配置方案_{timestamp}.csv")
        generator.generate_csv(result_df, csv_path)
        print(f"\n配置方案已保存至: {csv_path}")

        pdf_path = os.path.join(Config.OUTPUT_DIR, f"配置报告_{timestamp}.pdf")
        generator.generate_pdf(result_df, weights, etf_names, pdf_path)
        print(f"PDF报告已保存至: {pdf_path}")

if __name__ == "__main__":
    import sys
    engine = AllWeatherEngine(Config.DEFAULT_ETF_LIST)
    try:
        amount_input = input("请输入配置总金额（元）：")
        amount = float(amount_input)
    except:
        print("输入错误")
        sys.exit(1)
        
    results = engine.run(amount)
    if results:
        print("\n配置方案:")
        print(results["result_df"].to_string(index=False))
        print(f"\n预估年化收益率: {results['metrics']['annualized_return']*100:.2f}%")
        print(f"预估年化波动率 (风险): {results['metrics']['annualized_risk']*100:.2f}%")
        engine.save_reports(results["result_df"], results["weights"], results["etf_names"], amount)