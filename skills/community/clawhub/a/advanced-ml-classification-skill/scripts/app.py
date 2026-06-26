#!/usr/bin/env python3
"""Streamlit 前端示例：AdvancedMLClassificationSkill。"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from advanced_ml_skill import AdvancedMLClassificationSkill


st.set_page_config(page_title="轻量化AI分类预测平台", page_icon="📊", layout="wide")

st.title("📊 轻量化AI分类预测平台")
st.caption("自动训练、算法对比、交叉验证、参数搜索、特征重要性与中文解读")

with st.sidebar:
    st.header("基础配置")
    target_col = st.text_input("目标列名", value="label")
    algorithms = st.multiselect(
        "选择算法",
        options=AdvancedMLClassificationSkill.DEFAULT_ALGORITHMS,
        default=AdvancedMLClassificationSkill.DEFAULT_ALGORITHMS,
    )
    test_size = st.slider("测试集比例", min_value=0.1, max_value=0.5, value=0.2, step=0.05)
    random_state = st.number_input("随机种子", min_value=0, max_value=99999, value=42, step=1)
    openai_api_key = st.text_input("OpenAI API Key（可选）", type="password")

    st.divider()
    st.header("交叉验证（可选）")
    enable_cv = st.checkbox("启用交叉验证", value=False)
    cv_method = st.selectbox(
        "交叉验证方式",
        options=["StratifiedKFold", "KFold", "RepeatedStratifiedKFold"],
        index=0,
        disabled=not enable_cv,
    )
    cv_folds = st.slider("CV 折数", min_value=2, max_value=10, value=5, disabled=not enable_cv)
    cv_repeats = st.slider(
        "重复次数（仅 RepeatedStratifiedKFold 生效）",
        min_value=1,
        max_value=6,
        value=2,
        disabled=(not enable_cv or cv_method != "RepeatedStratifiedKFold"),
    )
    cv_scoring = st.selectbox(
        "CV 评分指标",
        options=["accuracy", "f1_weighted", "precision_weighted", "recall_weighted"],
        index=0,
        disabled=not enable_cv,
    )

    st.divider()
    st.header("参数搜索（可选）")
    enable_search = st.checkbox("启用参数搜索", value=False)
    search_method = st.selectbox(
        "搜索方式",
        options=["GridSearchCV", "RandomizedSearchCV"],
        index=0,
        disabled=not enable_search,
    )
    search_cv = st.slider(
        "搜索 CV 折数",
        min_value=2,
        max_value=8,
        value=3,
        disabled=not enable_search,
    )
    search_n_iter = st.slider(
        "随机搜索迭代次数（RandomizedSearchCV 生效）",
        min_value=5,
        max_value=80,
        value=20,
        disabled=(not enable_search or search_method != "RandomizedSearchCV"),
    )
    search_scoring = st.selectbox(
        "搜索评分指标",
        options=["accuracy", "f1_weighted", "precision_weighted", "recall_weighted"],
        index=0,
        disabled=not enable_search,
    )

    st.divider()
    feature_importance_enabled = st.checkbox("计算特征重要性排序", value=True)

st.subheader("数据输入")
uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])
manual_path = st.text_input("或输入本地 CSV 路径", value="")
st.caption("可直接试用：./demo.csv  |  ./demo_binary.csv  |  ./demo_multiclass.csv  |  ./demo_complex.csv")

run_clicked = st.button("开始训练与评估", type="primary")

if run_clicked:
    if uploaded_file is None and not manual_path.strip():
        st.error("请先上传 CSV 文件或填写本地路径。")
        st.stop()

    if not target_col.strip():
        st.error("请填写目标列名。")
        st.stop()

    data_path = manual_path.strip()

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            data_path = str(Path(tmp.name))

    try:
        skill = AdvancedMLClassificationSkill(
            data_path=data_path,
            target_col=target_col.strip(),
            algorithms=algorithms,
            test_size=test_size,
            random_state=int(random_state),
            openai_api_key=openai_api_key.strip() or None,
            cv_options={
                "enabled": enable_cv,
                "method": cv_method,
                "folds": cv_folds,
                "repeats": cv_repeats,
                "scoring": cv_scoring,
            },
            search_options={
                "enabled": enable_search,
                "method": search_method,
                "cv": search_cv,
                "n_iter": search_n_iter,
                "scoring": search_scoring,
            },
            feature_importance_enabled=feature_importance_enabled,
        )

        with st.spinner("模型训练中，请稍候..."):
            result = skill.run()

        st.success("任务完成！")

        st.subheader("算法准确率对比")
        rows = []
        for algo, score in result["accuracy_results"].items():
            error = skill.execution_errors.get(algo, "")
            cv_score = result.get("cv_results", {}).get(algo)
            search_info = result.get("search_results", {}).get(algo, {})
            rows.append(
                {
                    "算法": algo,
                    "测试集准确率": f"{score:.4f}" if isinstance(score, float) else "失败",
                    "CV 平均分": f"{cv_score:.4f}" if isinstance(cv_score, float) else "-",
                    "搜索最优分": (
                        f"{search_info.get('best_score'):.4f}"
                        if isinstance(search_info.get("best_score"), float)
                        else "-"
                    ),
                    "错误信息": error,
                }
            )

        result_df = pd.DataFrame(rows)
        st.dataframe(result_df, use_container_width=True)

        vis = result["visualization_data"]
        bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=vis["algorithms"],
                    y=vis["accuracies"],
                    text=[f"{value:.4f}" for value in vis["accuracies"]],
                    textposition="auto",
                    marker_color="#1f77b4",
                    name="测试集准确率",
                )
            ]
        )
        bar_fig.update_layout(title="测试集准确率柱状图", xaxis_title="算法", yaxis_title="准确率")
        st.plotly_chart(bar_fig, use_container_width=True)

        line_fig = go.Figure()
        line_fig.add_trace(
            go.Scatter(
                x=vis["algorithms"],
                y=vis["accuracies"],
                mode="lines+markers",
                line={"color": "#ff7f0e", "width": 3},
                name="测试集准确率",
            )
        )

        if enable_cv:
            cv_points = [value for value in vis.get("cv_scores", []) if isinstance(value, float)]
            if cv_points:
                line_fig.add_trace(
                    go.Scatter(
                        x=vis["algorithms"],
                        y=vis.get("cv_scores", []),
                        mode="lines+markers",
                        line={"color": "#2ca02c", "width": 2, "dash": "dash"},
                        name="CV 平均分",
                    )
                )

        line_fig.update_layout(title="准确率趋势图", xaxis_title="算法", yaxis_title="分数")
        st.plotly_chart(line_fig, use_container_width=True)

        if enable_search and result.get("search_results"):
            st.subheader("参数搜索最优结果")
            search_rows = []
            for algo, info in result["search_results"].items():
                search_rows.append(
                    {
                        "算法": algo,
                        "最优分": info.get("best_score"),
                        "最优参数": info.get("best_params"),
                    }
                )
            st.dataframe(pd.DataFrame(search_rows), use_container_width=True)

        feature_info = result.get("feature_importance") or {}
        feature_items = feature_info.get("items") or []
        if feature_items:
            st.subheader(f"特征重要性排序（算法：{feature_info.get('algorithm', 'N/A')}）")
            top_n = st.slider("展示前 N 个特征", min_value=5, max_value=30, value=12, step=1)
            top_items = feature_items[:top_n]
            fi_df = pd.DataFrame(top_items)
            st.dataframe(fi_df, use_container_width=True)

            fi_fig = go.Figure(
                data=[
                    go.Bar(
                        x=fi_df["importance"],
                        y=fi_df["feature"],
                        orientation="h",
                        marker_color="#17becf",
                    )
                ]
            )
            fi_fig.update_layout(
                title="Top 特征重要性",
                xaxis_title="Permutation Importance",
                yaxis_title="特征",
                yaxis={"autorange": "reversed"},
            )
            st.plotly_chart(fi_fig, use_container_width=True)

        st.subheader("结果解读（新手友好）")
        st.write(result["interpretation"])

        st.subheader("生成的训练代码")
        for algo_name, code in result["generated_codes"].items():
            with st.expander(f"查看 {algo_name} 代码"):
                st.code(code, language="python")

    except Exception as exc:
        st.exception(exc)
