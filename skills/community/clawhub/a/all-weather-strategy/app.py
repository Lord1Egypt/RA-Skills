import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import sys
import os
# Add scripts directory to path for marketplace structure
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from engine import AllWeatherEngine, Config, ReportGenerator

# Page Config
st.set_page_config(page_title="全天候投资配置系统", layout="wide")

# Sidebar - Parameters
st.sidebar.header("配置参数")

# ETF Pool Editing
default_etf_str = "\n".join(Config.DEFAULT_ETF_LIST)
etf_input = st.sidebar.text_area("ETF 标的池 (每行一个代码)", value=default_etf_str, height=200)
etf_list = [s.strip() for s in etf_input.split("\n") if s.strip()]

# Total Amount
total_amount = st.sidebar.number_input("拟配置总金额 (元)", min_value=100.0, value=10000.0, step=1000.0)

# Lookback Period
lookback_days = st.sidebar.slider("回看时长 (天)", min_value=90, max_value=1095, value=365)

# Main UI
st.title("🛡️ 全天候 ETF 资产配置系统")
st.markdown("""
依据 **风险平配 (Risk Parity)** 原理，自动计算各大类资产 ETF 的最优配置权重。
""")

if st.sidebar.button("开始计算"):
    if not etf_list:
        st.error("请输入至少一个 ETF 代码")
    else:
        # Progress Bar and Status
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(progress, text):
            progress_bar.progress(progress)
            status_text.text(text)

        # Initialize Engine
        engine = AllWeatherEngine(etf_list)
        
        # Execute Strategy
        results = engine.run(
            total_amount=total_amount, 
            lookback_days=lookback_days, 
            progress_callback=update_progress
        )

        if results:
            st.success("配置方案计算完成！")
            
            # 1. Metrics Displays
            m1, m2 = st.columns(2)
            ret = results['metrics']['annualized_return'] * 100
            risk = results['metrics']['annualized_risk'] * 100
            m1.metric("预估年化配置收益", f"{ret:.2f}%")
            m2.metric("配置组合年化风险 (波动率)", f"{risk:.2f}%")

            # 2. Results Table
            st.subheader("📊 配置方案详情")
            st.table(results['result_df'])

            # 3. Pie Chart
            st.subheader("🥧 权重分布可视化")
            
            # Prepare data for pie chart
            sorted_weights = results['weights']
            sorted_labels = [f"{results['etf_names'][code]}({code})" for code in results['result_df']['ETF代码']]
            
            # Use ReportGenerator's method to create chart
            gen = ReportGenerator(Config.register_chinese_font(), total_amount)
            wrapped_labels = [gen.wrap_text(label) for label in sorted_labels]
            
            fig = gen.create_pie_chart(sorted_weights, wrapped_labels)
            st.pyplot(fig)

            # 4. Export Options
            st.subheader("💾 报告导出")
            col1, col2 = st.columns(2)
            
            # CSV Download
            timestamp = datetime.now().strftime('%Y%m%d')
            csv_data = results['result_df'].to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            col1.download_button(
                label="下载 CSV 方案",
                data=csv_data,
                file_name=f"AllWeather_Plan_{timestamp}.csv",
                mime="text/csv"
            )

            # Note: PDF generation would require file writing/reading locally, 
            # for now we focus on the web UI experience.
            st.info("💡 提示：如需 PDF 详尽报告，请点击上方下载方案或在后台导出。")
        else:
            st.error("计算失败，请检查 ETF 代码是否正确或网络是否通畅。")

# Custom CSS for aesthetic
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Footer Copyright
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{Config.COPYRIGHT}**")
st.sidebar.caption(f"Author: {Config.AUTHOR}")
