# Bioinformatics Plotting Skill (生信绘图)

## Overview

This skill provides comprehensive knowledge of bioinformatics data visualization tools and techniques, based on the 微生信/SRplot platform (https://www.bioinformatics.com.cn/).

- **Platform:** 微生信/SRplot - Free online bioinformatics plotting platform
- **Published:** PLoS One 2023
- **Users:** 150,000+
- **Templates:** 320 plot types and analysis tools
- **Usage:** Select tool → Upload data → Adjust parameters → Download figure

## When to Use This Skill

- User needs to visualize bioinformatics data (RNA-seq, ChIP-seq, genome, clinical, etc.)
- User asks about which plot type to use for their data
- User wants to know how to create a specific bioinformatics figure
- User needs to choose between similar plot types for their analysis
- User is preparing figures for a bioinformatics research paper

## Plot Category Decision Guide

```
Data Type → Recommended Plot:
- Differential expression → Volcano plot, Heatmap, MA plot
- Gene expression comparison → Box/Violin plot, Heatmap
- Enrichment results → Bubble plot, Bar plot, Chord diagram
- Survival analysis → KM curve, Forest plot, Nomogram
- Genome distribution → Circos, Manhattan, Chromosome plot
- Sample clustering → PCA, t-SNE, UMAP, Heatmap
- Set overlap → Venn diagram, UpSet plot
- Gene interaction → Network plot, Sankey, Chord
- Time series → Line plot, Area plot, Streamgraph
- Clinical prediction → ROC, TimeROC, Nomogram, Risk score
- Mutation data → Oncoplot, Lollipop, MAF summary
- Single cell → UMAP/t-SNE, Volcano, Feature plot
- Geographic data → China/World/Province map
```

## Complete Plot Catalog

### 柱状图/条形图 (Bar/Column Charts) — 57 tools

**适用场景:** 用于比较不同组之间的数值大小，展示频率、计数或比例

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| errorbar柱状图 | errorbar | 免费在线绘制带误差棒的柱状图（bar with errorbar） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bar_with_errorbar_plot_023) |
| 误差棒 | errorbar | 免费在线绘制误差棒图（errorbar） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_errorbar_plot_025) |
| 人口金字塔 | population pyramids | 免费在线绘制双Y轴两侧条形图（人口金字塔图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dual_y_axis_horizontal_bar_plot_037) |
| 填充柱状图 | link fill bar | 免费在线绘制带有连线/填充的垂直堆叠柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_stackbar_with_links_and_fill_plot_038) |
| 带bar的饼图 | bar of pie | 在线绘制带bar的饼图（bar of pie） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bar_of_pie_plot_151) |
| 漏斗图 | funnel | 免费在线绘制漏斗图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_funnel_plot_005) |
| 蝴蝶图 | butterfly horizontal bar | 在线绘制蝴蝶图（butterfly bar plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_butterfly_horizontal_bar_plot_056) |
| 垂直柱状图 | vertical bar | 在线绘制基本柱状图，带趋势线 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_one_group_vertical_bar_with_trend_061) |
| 垂直棒棒糖图 | vertical lollipop | 在线绘制垂直棒棒糖图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_lollipop_chart_065) |
| 水平棒棒糖图 | horizontal lollipop | 在线绘制水平棒棒糖图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_lollipop_chart_066) |
| 相关系数棒棒糖图 | correlation | 在线免费线绘制相关系数点线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_corrlation_dot_line_054) |
| 极坐标柱状图，疫情图 | polar bar | 在线绘制极坐标柱状图，疫情图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_polar_barplot_072) |
| 多组垂直柱状图 | bar plot | 在线绘制多组柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_group_vertical_barplots_073) |
| 点状垂直柱状图 | dot bar | 在线绘制垂直点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_dot_bar_plot_074) |
| 堆叠柱状图 | vertical stack bar | 免费在线绘制堆叠柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_stack_bar_plot_075) |
| 堆叠条形图 | horizontal stack bar | 在线绘制水平堆叠柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_stack_bar_plot_076) |
| 点状水平条形图 | dot bar | 在线绘制水平点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_dot_bar_plot_077) |
| 子弹图 | bullet chart | 在线绘制子弹图（bullet chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bullet_chart_078) |
| 三维柱状图 | 3D bar | 在线绘制基本3D柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_group_vertical_3d_barplots_080) |
| 底部汇聚柱状图 | aggregation bar | 在线绘制底部汇聚柱状图图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bottom_aggregation_bar_plot_153) |
| 三维柱状图 | 3d bar | 在线绘制类似房子的三维柱状图， | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_building_3d_bar_plot_136) |
| 梯形漏斗图 | trapezoid funnel | 在线免费绘制梯形漏斗图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_trapezoid_funnel_plot_006) |
| 双向条形图 | bar plot | 在线绘制左右双向条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_left_right_bar_plot_100) |
| 多组水平条形图 | horizontal bar | 在线绘制多组条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_group_horizontal_bar_plot_208) |
| 三角锥柱状图 | triangle bar | 在线绘制三角锥柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_triangle_bar_plot_116) |
| 带Y轴截断的柱状图 | 截断 | 在线绘制带截断的（多组）柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_group_vertical_barplots_with_truncation_117) |
| 分类+条形组合图 | bar | 免费在线绘制二元，三元分类+bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_category_and_bar_plot_132) |
| 双X轴bar和line图 | 双轴 GO Pathway | 免费在线绘制双X轴go，pathway条形图加线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dual_x_axis_go_pathway_bar_line_plot_139) |
| 24小时极坐标bar图 | 24 hour polar bar | 免费在线绘制24小时极坐标bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_24h_polar_bar_plot_141) |
| 二元矩阵+双侧bar图 | matrix bar | 在线绘制矩阵+顶部bar+右侧bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_moA_matrix_with_top_right_bars_plot_146) |
| 雪糕柱状图 | bar | 在线绘制雪糕bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_xuegao_bar_plot_152) |
| 铅笔柱状图 | pencil bar | 在线绘制铅笔柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pencil_bar_plot_154) |
| 水平铅笔条形图 | pencil bar | 在线绘制水平立体感条形图（铅笔图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_pencil_bar_plot_174) |
| 带背景的茎叶柱状图 | stem bar with background | 在线绘制带背景的茎叶柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_stem_bar_with_background_plot_137) |
| 上下柱状图 | up down bar | 在线绘制上调、下调双向柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_up_down_bar_plot_217) |
| 双Y轴柱状图+折线图 | dual y bar & line | 在线绘制双Y轴柱状图+折线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dual_y_axis_bar_and_line_plot_231) |
| 曲线连接的填充堆叠柱状图 | curve linked stack bar | 在线绘制带连线的堆叠柱状图（stack bars） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_curve_filled_stack_bar_diagram_plot_234) |
| 扇形图，任意角度 | fan diagram | 在线绘制扇形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_fan_diagram_plot_173) |
| 嵌套两组errorbar图 | nested errorbar | 在线绘制两组嵌套errorbar | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_nested_two_group_error_bar_plot_236) |
| 带饼图的柱状图 | bar pie | 在线绘制带饼图的柱状图（bar with pie plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bar_with_pie_plot_182) |
| 2.5d柱状图 | bar | 在线绘制2.5D bar图，科技感 | [在线绘制](https://www.bioinformatics.com.cn/plot_advanced_stack_bars_221) |
| 极坐标柱状图 | polar bar | 在线绘制多组极坐标柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_group_bars_plot_226) |
| 字母标注bar图，box，小提琴图 | sig letter bar box violin | 在线绘制带显著字母标注的柱状图，box图和小提琴图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_sig_letter_bar_box_violin_plot_273) |
| 堆叠errorbar | stack errorbar | 在线绘制堆叠errorbar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_stack_error_bar_plot_276) |
| 两组学联合bar+dot图 | mRNA atac merip combined bar dot | 在线绘制两种组学联合分析条形点图（mRNA vs ATAC/ChIP/MeRIP/质谱等） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_omics_combined_bar_dot_plot_282) |
| 双Y轴柱状图 | dual y axis bar | 在线绘制双Y轴柱状图（bar plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dual_y_axis_bar_plot_284) |
| 渐变条形图 | gradient bar | 在线绘制p值渐变条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gradient_bar_plot_286) |
| 多组errorbar图 | errorbar | 在线绘制多组误差棒比较图 | [在线绘制](https://www.bioinformatics.com.cn/plot_multi_groups_of_errorbar_298) |
| 拷贝数变异bar图 | CNV gain and loss | 在线绘制基因拷贝数变异（CNV）获得（gain）和缺失（loss）频率柱状图 | [在线绘制](https://www.bioinformatics.com.cn/basic_copy_number_variation_gain_and_loss_bar_plot) |
| 多组堆叠柱状图 | group stack bar | 在线绘制多组堆叠柱状图 | [在线绘制](https://www.bioinformatics.com.cn/basic_group_stack_bar_plot) |
| 多组errorbar图 | group errorbar | 在线绘制多组errorbar，带显著性 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_group_errorbar_with_pvalue) |
| 堆叠柱状图+连线路径 | stack bar + links | 在线绘制带路径的堆叠柱状图，展示患者状态 | [在线绘制](https://www.bioinformatics.com.cn/basic_stack_bar_with_links_plot) |
| 双Y轴GO柱状图 | dual y go term bar | 在线绘制GO BP, CC, MF term百分比，基因数双Y轴bar图 | [在线绘制](https://www.bioinformatics.com.cn/basic_dual_y_go_bp_cc_mf_gene_percent_number_bar_plot) |
| 多组极坐标柱状图 | multi group polar bar | 在线绘制多组极坐标（堆叠）柱状图 | [在线绘制](https://www.bioinformatics.com.cn/basic_multi_group_polar_bar_plot) |
| 水平条形图 | horizontal bar | 在线绘制水平柱状图、条形图（BP、CC、MF三合一图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_bar_062) |
| 矩形漏斗图 | rectangle funnel | 在线绘制矩形漏斗图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_rectangle_funnel_plot_007) |
| 基因上下调柱状图 | gene miRNA regulation | 免费在线绘制基因上下调柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gene_up_down_bar_plot_014) |

### 饼图/甜甜圈图/树图 (Pie/Donut/Treemap) — 19 tools

**适用场景:** 用于展示部分与整体的比例关系

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 矩阵饼图 | pie matrix | 免费在线绘制矩阵形式饼图（pie matrix） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pie_matrix_plot_033) |
| 华夫饼图 | waffle | 在线绘制华夫饼图（waffle chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_waffle_chart_plot_050) |
| treemap | treemap | 在线绘制树图（treemap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_treemap_063) |
| 甜甜圈图 | donut chart | 免费在线绘制甜甜圈图（donut） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_donut_chart_plot_051) |
| 双层饼图 | two layer pie | 免费在线绘制双层饼图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_layer_pie_plot_003) |
| 圆形比例图 | percentage half circle | 在线绘制圆形（半圆形）华夫饼图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_waffle_plot_089) |
| 双层甜甜圈图 | two layer donut | 免费在线绘制双层甜甜圈图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_layer_donut_chart_004) |
| 维诺图 | voronoi treemaps | 在线绘制维诺图（voronoi treemap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_voronoi_treemaps_plot_079) |
| 多类型饼图 | 轨道图，扇形图 | 免费在线绘制多类型2D饼图（2D pie） | [在线绘制](https://www.bioinformatics.com.cn/plot_multi_types_2d_pie_by_tastypie_128) |
| 圆形堆叠图 | stack circle | 在线绘制circle packing图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_packing_129) |
| 图标华夫饼图 | icon waffle | 在线绘制icon图标华夫饼图（icon waffle chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_icon_waffle_chart_plot_228) |
| 带连线注释的甜甜圈 | donut pie | 在线绘制带连线注释的饼图、甜甜圈图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_donut_chart_with_connection_line_annotation_plot_183) |
| 大饼拉小饼图 | pie | 在线绘制大饼拉小饼图（pie of pie） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pie_of_pie_plot_186) |
| 渐变树图 | gradient treemap | 在线绘制渐变颜色树图（treemap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gradient_color_treemap_plot_246) |
| 动态旭日图 | plotly sunburst | 在线python plotly绘制旭日图（sunburst chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_plotly_sunburst_chart_252) |
| 圆填充图 | circle packing | 在线绘制单层圆填充图（circle packing） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_one_level_circle_packing_plot) |
| 摩天轮甜甜圈图 | ferris_wheel donut | 在线绘制摩天轮图展示基因上调，下调（Ferris wheel donut chart） | [在线绘制](https://www.bioinformatics.com.cn/basic_ferris_wheel_gene_up_down_circle_donut_chart) |
| 3D饼图 | 3D pie | 免费在线绘制3D饼图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_3d_pie_plot_020) |
| 2D饼图 | 2D pie | 免费在线绘制二维饼图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_2D_pie_plot_002) |

### 折线图/面积图 (Line/Area Charts) — 16 tools

**适用场景:** 用于展示随时间或条件变化的趋势

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 成比例面积图 | proportional area chart | 免费在线绘制圆形，正方形比例面积图（proportional area chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_proportional_circle_squre_area_chart_021) |
| 两组成比例面积图 | proportional circle area | 在线绘制两组半圆形比例面积图（proportional area chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_2group_proportional_circle_area_chart_022) |
| 4组面积图 | squre area | 免费在线绘制4个正方形一组的比例面积图（proportional area chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_x4_proportional_squre_area_chart_030) |
| 散点图带倍数变化线 | scatter fold change | 在线绘制带倍数变化的散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scatter_plot_with_fc_lines_044) |
| 一条/多条线图 | multi-line | 免费在线绘制简单线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_one_or_multi_lines_055) |
| 填充线图 | filled area | 在线绘制填充线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_area_plot_057) |
| 3D面积图 | 3D area | 在线绘制三维面积图（3D area） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_3d_area_plot_058) |
| 堆叠面积图 | stack area | 在线绘制堆叠图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_area_stack_059) |
| 堆叠线图 | stack line | 免费在线绘制堆叠线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_line_stack_plot_060) |
| 双坐标基因表达图 | RNA-seq, PCR, dual Y | 在线绘制PCR，RNA-seq双Y坐标图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_PCR_RNAseq_dual_y_axis_plot_084) |
| 河流图 | streamgraph | 免费在线绘制河流图（streamgraph） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_streamgraph_plot_148) |
| 排序图 | bump chart rank | 免费在线绘制排序图（bump rank） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_bump_rank_chart_plot_149) |
| 双Y轴折线图 | dual y line plot | 在线绘制双Y轴折线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dual_y_axis_line_plot_189) |
| 多组数字标记折线图 | multi group number marker line | 在线绘制多组折线图（数字做为marker点） | [在线绘制](https://www.bioinformatics.com.cn/basic_multi_lines_with_number_as_marker) |
| 平滑线图 | smooth line | 免费在线绘制平滑点线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_smooth_line_001) |
| 瀑布图 | waterfall | 免费在线绘制瀑布图（waterfall） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_waterfall_chart_011) |

### 散点图 (Scatter Plots) — 14 tools

**适用场景:** 用于展示两个连续变量之间的关系

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| m6A和表达联合散点图 | m6A 甲基化 methylation 表达谱 | 在线绘制m6A甲基化和表达谱联合分析散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_m6a_exp_scatter_plot_088) |
| 分组_回归的散点图 | scatter fit group | 免费在线绘制带回归的多组数据散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_group_scatter_plot_041) |
| 散点图 | scatter plot R2 | 在线免费线绘制散点图，带线性拟合，曲线拟合 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scatter_plot_053) |
| 二元-三元类别图 | category plot | 免费在线绘制二元，三元分类图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_01_123_category_plot_008) |
| 三维散点图（带分类） | 3D scatter | 免费在线绘制三维散点图（3D scatter） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_3d_scatter_plot_091) |
| 排序散点图 | rank plot with labels | 在线绘制带标注的排序图（散点图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_rank_plot_with_labels_179) |
| 联合分析四象限图 | m6A mRNA 多组学 | 在线绘制组学联合分析四象限图（例如m6A-mRNA，m5C-mRNA，mRNA-蛋白等） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_omics_combined_four_quadrant_scatter_plot_238) |
| 九象限图 | nine quadrant | 在线绘制组学联合分析9象限图（例如m6A-mRNA，m5C-mRNA，mRNA-蛋白等） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_nine_quadrant_scatter_plot_201) |
| 密度散点图 | smooth scatter | 在线绘制平滑散点图（smooth scatter）图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_smooth_scatter_plot_198) |
| 三元图 | ternary | 在线绘制三元图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ternary_plot_243) |
| 多组配对散点图 | multi group paired scatter | 在线绘制多组左右配对连线散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_group_left_right_paired_scatter_plot_264) |
| 多颜色散点图 | multi color scatter | 在线绘制带颜色的多组散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_group_colored_scatter_plot_with_names_257) |
| 四象限图 | four quadrant | 免费在线绘制四象限散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_four_quadrant_scatter_plot_010) |
| 相关系数散点图 | pearson spearman coefficient correlation | 在线绘制多组数据相关系数散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pcc_scatter_plot_049) |

### 箱线图/小提琴图/分布图 (Box/Violin/Distribution) — 20 tools

**适用场景:** 用于展示数据分布特征和组间比较

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 小提琴图 | violin box | 免费在线绘制小提琴图（ggviolin） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ggviolin_plot_113) |
| 蜂群图 | beeswarm boxplot | 免费在线绘制带点的箱体图（beeswarm box） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_beeswarm_box_plot_027) |
| 核密度分布 | kernel density | 免费在线绘制核密度估计（Kernel density estimation） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_kernel_density_estimation_plot_036) |
| QQplot_正态分布 | qqplot | 免费在线绘制quantile-quantile图（Q-Q plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_quantile_quantile_qqplot_042) |
| 山脊线 | ridgeline plot joyplot | 免费在线绘制山脊图（ridgeline plot, Joyplot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ridgeline_plot_045) |
| 带连线的box图 | dot line box | 在线绘制带有数据点连线的box图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_boxplot_with_connection_lines_047) |
| 带hist，box的散点图 | scatter hist box density | 免费在线绘制带边界（density，histogram，boxplot）的散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scatter_with_marginal_histograms_plot_104) |
| 高级小提琴图 | violin | 免费在线绘制小提琴图，violin plot | [在线绘制](https://www.bioinformatics.com.cn/plot_advanced_vertical_horizontal_violin_plot_114) |
| 箱体图，盒子图 | boxplot, box | 在线绘制垂直、水平箱体图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_horizontal_box_plot_067) |
| 水平，垂直小提琴图 | violin | 免费在线绘制小提琴图（violin plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_horizontal_violin_plot_068) |
| 直方图，带拟合 | histogram, fit | 在线绘制直方图，带拟合 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_histogram_with_without_fit_069) |
| 雨云图 | raincloud | 在线绘制云雨图（raincloud plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_raincloud_plot_093) |
| 小提琴图 豆荚图 | half violin | 在线绘制half violin | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_half_violin_plot_097) |
| 带点箱体图 | 箱体图 box | 在线绘制带点，p值的多组box图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ggpubr_box_plot_123) |
| 高级雨云图 | raincloud violin | 在线绘制多组雨云图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_rain_cloud_plot_209) |
| 两组或多组比较box | two groups box | 在线绘制两组（或多组）比较box图（cibersort） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cibersort_two_group_comparison_box_plot_180) |
| 多组histogram | multi histogram | 在线绘制多个直方图，带拟合 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_histogram_with_without_fit_253) |
| 二维密度图 | 2d density | 在线绘制2D密度图，等高线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_2d_density_plot) |
| 多组两两比较beeswarm图 | group comparison beewarm | 在线绘制两组比较带王字的蜂群图（beeswarm） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_group_comparison_beeswarm_plot_with_pvalue) |
| 任意组比较beeswarm图 | group comparison beewarm | 在线绘制多组比较带王字的蜂群图（beeswarm） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_group_comparison_beeswarm_plot_with_pvalue) |

### 其他基础图 (Other Basic Charts) — 18 tools

**适用场景:** 相关系数、词云、雷达图等特殊图表

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 相关系数图 | correlation, corrplot | 在线绘制corrplot相关系数图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_corrplot_corrlation_plot_082) |
| 哑铃图 | dumbbell chart | 免费在线绘制哑铃图（dumbbell chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dumbbell_chart_032) |
| 气球图_气泡图 | ballon plot bubble plot | 免费在线绘制气泡图，气球图（ballon plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ballon_plot_048) |
| 雷达图 | radar chart | 在线绘制雷达图（radar chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_radar_chart_plot_052) |
| 茎叶图 | stem | 在线绘制茎叶图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_stem_plot_071) |
| 矩阵点图，气泡图 | dot plot | 在线绘制矩阵形式的点图（dot plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_matrix_dotplot_210) |
| 三联体DNA | triplex DNA | 在线搜索和绘制三联体DNA（triplex DNA） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_triplex_DNA_plot_096) |
| metaplot图 | MeRIP m6A metaplot | 在线绘制MeRIP-seq (m1A, m6A, m5C等）metaplot图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_merip_m6a_metaplot_013) |
| 词云，wordcloud | 词云，wordcloud | 在线绘制词云图（wordcloud），支持中英文 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_wordcloud_118) |
| 蚊香图，alpha | 螺旋 短肽 | 在线绘制多肽alpha helical wheel和wenxiang图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_alpha_helical_wheels_and_wenxiang_diagrams_119) |
| 双重序列比对螺旋图 | sparial sequence alignment | 在线绘制双重序列比对结果螺旋图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_paired_sequence_alignment_on_sparials_plot_125) |
| 圆形相关系数图 | circle correlation pearson | 在线绘制圆形相关系数图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_correlation_plot_133) |
| 样品类型cohort图 | cohort | 在线绘制样品状态(cohort types)图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cohort_types_plot_150) |
| 相关系数矩阵 | correlation corrplot | 在线绘制上三角，下三角数值矩阵图（相关系数图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_custom_range_corrlation_plot_224) |
| NCBI ORFfinder结果可视化 | orffinder | 在线NCBI ORFfinder结果可视化 | [在线绘制](https://www.bioinformatics.com.cn/plot_ncbi_orffinder_six_frame_translation_output_visualization_187) |
| 带显著性标注的相关系数图 | correlation pvalue | 在线绘制带p值显著性标注的相关系数图，支持行列不同 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_significant_level_labelled_correlation_plot_251) |
| 基因表达雷达图 | expression radar | 在线绘制基因表达雷达图（gene expression radar chart） | [在线绘制](https://www.bioinformatics.com.cn/plot_gene_expression_radar_chart_296) |
| 雷达图，蜘蛛图 | radar, spider chart | 在线绘制任意边雷达图（蜘蛛图） | [在线绘制](https://www.bioinformatics.com.cn/basic_spider_chart_radar_chat) |

### 热图 (Heatmaps) — 23 tools

**适用场景:** 用于展示矩阵数据的模式，基因表达、样本聚类

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 聚类图_热图 | cluster heatmap | 免费在线绘制聚类图(cluster)，热图(heatmap) | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cluster_heatmap_plot_024) |
| 风险得分三联图 | risk score | 在线绘制ggrisk风险得分三联图（risk score） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_risk_score_scatter_and_heatmap_three_in_one_plot_188) |
| 圆形聚类图 | circular heatmap | 免费在线绘制圆形聚类图(circular cluster) | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circular_cluster_heatmap_plot_070) |
| 矩阵热图 | matrix heatmap | 在线绘制矩阵热图（matrix heatmap），相关系数图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_matrix_heatmap_064) |
| SNP连锁不平衡 | SNP LDheatmap | 在线绘制连锁不平衡（倒）三角热图（LD heatmap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_LDheatmap_plot_094) |
| 日历热图 | calendar heatmap | 在线绘制日历热图（calendar heatmap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_calendar_heatmap_plot_098) |
| 脑区热图 | cerebro heatmap brain | 在线绘制不同大脑区域热图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cerebro_colormap_115) |
| 三角热图 | triangle heatmap | 在线绘制相关系数三角热图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_correlation_pvalue_triangle_heatmap_plot_143) |
| 带部分基因标注的热图 | heatmap cluster gene label | 在线绘制带几个基因标注的聚类图(cluster)，热图(heatmap) | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_heatmap_with_several_gene_labels_by_complexheatmap_plot_178) |
| 带cut的聚类热图 | cut heatmap | 在线绘制带cut的热图（heatmap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cutted_cluster_heatmap_plot_223) |
| 多分组临床热图 | clinical heatmap | 在线绘制多分类临床聚类热图(clinical heatmap) | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_group_clinical_heatmap_207) |
| 带行列注释条的热图 | gap heatmap | 在线绘制带gap的热图（heatmap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gapped_cluster_heatmap_plot_222) |
| 表达热图+趋势图 | heatmap trend time series | 在线绘制热图+趋势 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_heatmap_with_mfuzz_or_kmeans_cluster_lines_plot_218) |
| 表达热图+趋势图+注释 | heatmap trend go pathway | 在线绘制热图+趋势+GO或者Pathway等注释组合图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_heatmap_with_mfuzz_or_kmeans_cluster_lines_go_pathway_plot_219) |
| 热图+标记 | heatmap label text | 在线绘制带标注的聚类热图（heatmap） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_cluster_heatmap_with_labels_plot_249) |
| 热图+bar图组合 | heatmap bar | 在线绘制热图+条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_heatmap_and_bar_plot_267) |
| 左右双侧组合热图 | heatmap | 在线绘制左右组合热图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_left_right_dual_heatmap_plot_269) |
| 点棒热图 | dot bar heatmap | 在线绘制点棒热图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dotbar_heatmap_plot_270) |
| 染色体密度+标记 | ideogram heatmap marker | 在线绘制human hg38染色体密度+marker标记图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ideogram_heatmap_marker_plot_287) |
| 相关系数圆形圈图 | correlation heatmap | 在线绘制相关系数渐变圈图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_heatmap_with_labels_and_groups_plot_288) |
| 圆圈，三角热图 | special shape heatmap | 在线绘制特殊形状（圆形，三角形，菱形，五边形，六边形，椭圆）聚类热图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_special_shape_heatmap_289) |
| 热图+桑基图 | heatmap sankey diagram | 在线绘制热图桑基组合图（heatmap+sankey diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_heatmap_plus_sankey_diagram_294) |
| 配受体对互作热图 | ligand receptor interaction heatmap | 在线绘制受体配体对互作热图（ligand-receptor heatmap with links） | [在线绘制](https://www.bioinformatics.com.cn/plot_ligand_receptor_dual_heatmap_with_links_297) |

### 火山图 (Volcano Plots) — 11 tools

**适用场景:** 用于展示差异表达基因的fold change和显著性

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 带基因标注的火山图 | volcano plot | 免费在线绘制带标注的增强火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_enhanced_volcano_plot_138) |
| 渐变火山图 | gradient volcano plot | 在线绘制渐变火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gradient_color_volcano_plot_227) |
| 带基因标注的双火山图 | two linked volcano plot | 在线绘制带共同基因标注的双火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_label_genes_linked_two_volcano_plot_237) |
| 代谢火山图 | vip volcano plot | 在线绘制带vip的代谢火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_volcano_plot_with_vip_as_point_size_plot_241) |
| 双曲线火山图 | volcano plot | 在线绘制双曲线火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_volcano_plot_with_curve_242) |
| 单细胞cluster火山图 | scRNA cluster volcano plot | 在线绘制单细胞多cluster火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scrna_multi_volcano_plot_244) |
| 双色，四色火山图 | volcano plot | 在线绘制两种颜色或者四种颜色的火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_colors_or_four_colors_volcano_plot_248) |
| 单细胞marker火山图 | scRNA-seq marker volcano | 在线绘制单细胞marker基因火山图by scRNAtoolVis | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scrna_seq_marker_gene_vocalno_plot_by_scRNAtoolVis_261) |
| 单细胞火山图 | scRNA-seq volcano | 在线绘制单细胞火山图，极坐标火山图 by scRNAtoolVis | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_scrna_seq_vocalno_plot_by_scRNAtoolVis_263) |
| 多类别点标注火山图 | multi-colored volcano | 在线绘制多类别标注火山图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_class_colored_volcano_plot_268) |
| 三颜色火山图 | volcano plot | 在线绘制三颜色火山图（volcano plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_3_color_volcano_plot_086) |

### 富集分析图 (Enrichment Analysis) — 31 tools

**适用场景:** 用于GO/KEGG/GSEA功能富集分析结果可视化

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 富集气泡图 | enrichment dot bubble | 在线绘制GO，Pathway富集结果气泡图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gopathway_enrichment_bubbleplot_081) |
| BP,CC,MF三合一 | enrichement GO term | 免费在线绘制富集GO term BP, CC, MF三合一柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_GO_term_bp_cc_mf_bar_plot_046) |
| GO_Pathway弦图 | Gene Ontology, chord | 在线绘制GO弦图（chord） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_GOplot_chord_plot_085) |
| GSEA基因集富集分析 | gsea gene set genesets | 在线任意物种，任意基因集富集分析（gene set enrichment analysis，GSEA）绘图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gene_set_enrichment_analysis_gsea_analysis_193) |
| pathway加颜色 | KEGG pathway map pathview | Pathview在线渲染KEGG pathway map | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_kegg_pathway_map_by_pathview_092) |
| 多类型气泡图 | 气泡图 go pathway | 在线绘制多分类GO，Pathway富集结果气泡图 | [在线绘制](https://www.bioinformatics.com.cn/plot_multi_gopathway_enrichment_bubbleplot_016) |
| GO,KEGG点线图 | GO BP CC MF KEGG | 在线绘制GO,KEGG富集条形带点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_GO_KEGG_bar_dot_plot_111) |
| 富集桑基图_气泡图 | sankey dot pathway enrichment | 在线绘制GO，pathway富集结果桑基气泡图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_go_pathway_sankey_dot_plot_121) |
| pathway分类汇总图 | kegg pathway | 免费在线绘制pathway富集结果分类图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pathway_enrichment_categorical_bar_plot_124) |
| GO_Pathway富集圈图 | enrichment circle | 在线绘制GO，pathway富集结果圆形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_go_pathway_circlize_plot_140) |
| GSEA_GSVA双向条形图 | GSEA GSVA | 在线绘制GSEA，GSVA双向bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gsea_gsva_dual_bar_plot_142) |
| GO circle | GO圈图 | 在线绘制GO circle图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_GOplot_circle_plot_144) |
| 富集分析cnet图 | enrichment cnetplot | 在线绘制clusterprofiler go kegg富集分析cnet图 | [在线绘制](https://www.bioinformatics.com.cn/plot_clusterprofiler_go_kegg_enrichment_analysis_cnetplot_232) |
| GOcluster圈图 | gocluster goplot | 在线绘制GO cluster图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_goplot_gocluster_plot_190) |
| BP,CC,MF三合一 | GO三合一图 | 在线绘制GO BP CC MF三合一双侧条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_GO_term_bp_cc_mf_left_right_bar_plot_191) |
| KEGG pathway二级分类汇总 | kegg pathway | 在线绘制KEGG pathway富集结果二级分类汇总图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_pathway_enrichment_second_class_summary_bar_plot_206) |
| GSEA网络图 | gsea geneset network | 在线绘制clusterprofiler GSEA结果网络图，aPEAR包 | [在线绘制](https://www.bioinformatics.com.cn/plot_network_visualization_of_gsea_results_from_clusterprofiler_by_apear_212) |
| gsea标记基因 | gsea gene | 在线绘制带标注基因的GSEA图，GseaVis | [在线绘制](https://www.bioinformatics.com.cn/plot_advanced_gsea_plot_from_clusterprofiler_results_by_gseavis_216) |
| BP,CC,MF三合一 | go bp cc mf bars | 在线绘制GO富集条形图，带背景，标基因数 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_go_horizontal_bar_with_labels_247) |
| 带基因名的富集条形图 | kegg enrichment go gene bar | GO,Pthway富集分析条形图加基因 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_go_kegg_enrichment_hbar_with_genes_250) |
| 水平分面气泡图 | bubble plot | 在线绘制GO，Pathway富集结果气泡图水平分面 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_horizontal_facet_kegg_go_bubble_plot_240) |
| 气泡图 | enrichment dot | 在线绘制富集气泡图，文字标注在气泡上 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_enrichment_bubble_plot_126) |
| GSEA NES柱状图+FDR点图 | GSEA NES FDR bar dot | 在线绘制GSEA NES FDR组合bar dot图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gsea_nes_fdr_bar_dot_plot_283) |
| emapplot网络图 | emapplot | 在线绘制clusterprofiler go kegg富集分析emap图 | [在线绘制](https://www.bioinformatics.com.cn/plot_clusterprofiler_go_kegg_enrichment_analysis_emapplot_233) |
| 高级富集bar图 | enrichment bar | 在线绘制高级富集分析条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_advanced_enrichment_bar_plot_290) |
| stamp差异bar图 | stamp differences | 在线绘制STAMP差异分析条形+置信区间图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_stamp_plot_291) |
| 富集分析彗星图 | enrichment comet plot | 在线绘制富集分析结果彗星图（comet plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_enrichment_comet_plot_292) |
| GSEA富集山峦图 | GSEA NES ridge plot | 在线绘制GSEA富集分析山峦图 | [在线绘制](https://www.bioinformatics.com.cn/plot_gsea_nes_p_log2fc_ridge_293) |
| GO气泡图 | GO bubble | 在线绘制GOplot GO气泡图（GO bubble） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_goplot_gobuble_plot) |
| 通路影响气泡图 | pathway impact dot plot | 在线绘制代谢组学pathway impact vs p值气泡图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_metabolism_pathway_impact_dot_plot) |
| 带颜色富集条形图 | bar with color gredient | 在线绘制以p/FDR为颜色梯度的条形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_hbar_with_pvalue_color_plot_105) |

### 韦恩图/文氏图 (Venn Diagrams) — 10 tools

**适用场景:** 用于展示多个集合之间的交集和并集

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 4/5/6/7元文恩图 | venn diagram | 在线绘制4个、5个、6个、7个数据集的venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_4_5_6_7_venn_diagram_184) |
| 峰重叠文氏图 | peak overlap, venn diagram | 免费在线绘制基因组区（peaks）重叠venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_genomic_regions_overlap_venn_diagram_026) |
| 多类型文氏图 | vennerable | 免费在线绘制ChowRuskey venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multi_type_venn_diagram_103) |
| 网络venn图 | network venn diagram | 在线绘制网络venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_network_venn_diagram_272) |
| 2,3,4,5文氏图 | venn diagram, euler | 在线绘制2,3,4,5个数据集的文氏图（venn diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_2_3_4_5_venn_diagram_281) |
| 文恩图+条形图 | venn bar | 在线绘制两个数据集的venn+bar图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_datasets_venn_diagram_plus_horizontal_bar_plot_285) |
| 饼图+弧venn图 | pie arc venn | 在线绘制饼图+弧线 venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_pie_arc_venn_plot_295) |
| 垂直两圆文恩图 | vertical venn diagram | 在线绘制垂直双圆venn图（vertical venn diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_vertical_two_circle_venn_diagram) |
| 成比例面积文氏图 | proportional venn diagram | 免费在线绘制2个或3个圈的成面积比例venn图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_proportional_2_or_3_venn_diagram_028) |
| upsetR | upsetR set | Error | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_upsetR_plot_009) |

### 基因组图 (Genome/Mutation) — 21 tools

**适用场景:** 用于基因组位置、突变、染色体分布可视化

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 染色体分布图 | peak chromosome distribution | 在线绘制上调，下调peak染色体分布图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_up_down_gene_chromsome_distribution_plot_095) |
| 双通道circos柱状图 | 2 tracks circos histogram | 免费在线绘制两个track的circos柱状图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_2_tracks_circos_histogram_plot_031) |
| 花瓣图 | flower plot | 免费在线绘制花瓣图（flower plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_flower_plot_039) |
| motif_logo | DNA RNA 氨基酸 | 在线motifStack绘制DNA,RNA,Protein motif logo | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dna_rna_protein_motif_043) |
| 峰染色体分布图 | ideogram chromosome | 在线绘制peak染色体分布图（chromosome ideogram plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_peak_chromosome_distribution_plot_087) |
| UPGMA聚类 | 微生物多样性 | UPGMA聚类 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_upgma_clustering_plot_102) |
| SNP密度图 | SNP density | 在线绘制SNP密度（snp density）by CMplot | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_SNP_density_by_CMplot_107) |
| 片段染色体分布图 | SNP chromosome distribution | 在线绘制不带着丝粒的简单基因组位点染色体分布图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multitype_chromosome_distribution_plot_without_centromere_108) |
| 片段染色体分布图-着丝粒 | SNP chromosome distribution | 在线绘制带着丝粒的简单基因组位点染色体分布图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_multitype_chromosome_distribution_plot_with_centromere_109) |
| 曼哈顿图 | Manhattan plot | 在线绘制曼哈顿图（Manhattan plot）by CMplot | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_Manhattan_Plot_by_CMplot_110) |
| 物种累积曲线 | species accumulation curves | 免费在线绘制物种累积曲线（Species accumulation curves） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_species_accumulation_curves_plot_127) |
| MAF突变汇总图 | MAF summary plot | 在线绘制MAF突变注释汇总图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_maf_summary_plot_134) |
| MAF突变瀑布图 | oncoplot | 在线绘制MAF突变注释瀑布图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_maf_oncoplot_135) |
| 物种稀释曲线 | species rare curve | 免费在线绘制物种稀释曲线（Species rarecurve） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_species_rarecurve_plot_147) |
| 带基因名的Rcircos图 | Rcircos 染色体 基因 | 在线绘制Rcircos染色体基因名circos图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_rcircos_chromosome_gene_name_plot_185) |
| 融合基因circos图 | fusion genes | 在线绘制circlize融合基因circos图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circlize_fusion_gene_links_plot_213) |
| homer motif结果散点图 | homer motif scatter | 在线绘制homer motif结果散点图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_homer_motif_scatter_plot_220) |
| 突变棒棒糖图 | lollipop mutation | 在线棒棒糖蛋白质突变图（lollipop mutation diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_lollipop_mutation_diagram_090) |
| 花瓣图 | flower petal plot | 在线绘制花瓣图（polar area diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_petal_plot_277) |
| 染色体+bar组合图 | chromosome bar | 在线绘制染色体+bar组合图 | [在线绘制](https://www.bioinformatics.com.cn/basic_chromsome_position_and_bar_combined_plot) |
| 进化树，树状图 | dendrogram tree | 在线绘制dendrogram图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_dendrogram_plot_018) |

### 降维分析图 (Dimensionality Reduction) — 8 tools

**适用场景:** 用于高维数据的降维和聚类可视化

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 主成分分析 | principal components analysis | 在线绘制主成分分析图（Principal component analysis，PCA） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_PCA_plot_034) |
| PCA主成分分析 | PCA factor | 免费在线绘制主成分分析图（Principal components analysis，PCA） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_ggbiplot_PCA_plot_112) |
| 三维PCA | 3d pca | 在线绘制3D PCA图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_3d_pca_plot_196) |
| t-SNE降维 | t-SNE | 在线t-SNE（t-Distributed Stochastic Neighbor Embedding）降维、可视化 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_tsne_dimensionality_reduction_by_rtsne_202) |
| UMAP降维可视化 | umap | 在线UMAP（uniform manifold approximate projection）降维、可视化 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_umap_dimensionality_reduction_204) |
| 主坐标分析PCoA | pcoa | 在线绘制主坐标分析PCoA降维图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_PCoA_plot_035) |
| 非度量多维排列NMDS | nmds | 在线绘制非度量多维排列NMDS降维图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_nmds_plot_245) |
| PCA分析（三重复） | PCA convex hull | 在线绘制支持组内三重复的凸包主成分分析图（Principal component analysis，PCA） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_convex_hull_pca_plot) |

### 临床图 (Clinical Plots) — 9 tools

**适用场景:** 用于生存分析、ROC、风险模型等临床研究

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| KM生存曲线 | KM survival curve | 免费在线绘制Kaplan Meier(KM)生存曲线 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_kaplan_meier_survival_curve_plot_040) |
| 森林图 | forest plot hazard ratio | 在线绘制森林图（forest plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_forest_plot_099) |
| ROC曲线 | ROC曲线 AUC | 在线绘制ROC曲线 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_one_or_multi_ROC_curve_plot_106) |
| 时间依赖的ROC | timeROC ROC | 在线绘制timeROC | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_timeROC_curve_130) |
| 最佳cutoff生存曲线 | best cutoff kmplot | 在线绘制最佳cutoff Kaplan Meier(KM)生存曲线 | [在线绘制](https://www.bioinformatics.com.cn/plot_two_group_best_cutoff_kaplan_meier_survival_curve_plot_239) |
| 临床信息甜甜圈矩阵图 | clinical donut matrix | 在线绘制临床多组分类甜甜圈矩阵图 | [在线绘制](https://www.bioinformatics.com.cn/plot_clinical_info_table_to_donut_matrix_plot_265) |
| 基因排序图 | gene rank | 在线绘制基因排序图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_gene_rank_plot_266) |
| 肿瘤亚克隆鱼图 | tumor subclone fishplot | 在线绘制肿瘤克隆进化鱼图（fishplot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_tumor_evolution_fishplot_274) |
| 临床预测模型列线图 | nomogram calibration | 在线绘制临床生存列线图（clinical nomogram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_clinical_nomogram_279) |

### 网络图/关系图 (Network/Relationship) — 15 tools

**适用场景:** 用于展示基因、蛋白、通路之间的相互作用关系

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 环状RNA-miRNA图 | circRNA miRNA circle | 在线绘制circRNA - miRNA结合圆形图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circRNA_miRNA_ring_plot_083) |
| 多层圆形网络图 | circle network | 在线绘制多层从属关系（GO，pathway，物种等）圆圈网络图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_three_layer_circle_network_plot_200) |
| 基因表达连线图 | connection PCR RNA-seq | 免费在线绘制PCR基因表达连线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_expression_connection_lines_029) |
| 时序分析，cluster | mfuzz time series | Mfuzz时间序列聚类 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_mfuzz_soft_clustering_plot_101) |
| 左右连线图，直线，弧线 | arc link,line link | 在线绘制左右两列弧线图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_left_right_arc_links_plot_145) |
| 桑基图 | sankey diagram | 在线绘制桑基图（sankey diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_sankey_plot_229) |
| 弦图 | chord diagram | 在线绘制弦图（chord diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_chord_diagram_plot_230) |
| 圆形跑道图 | circle track | 在线绘制跑道图（circle track） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_circle_track_plot_175) |
| miRNA-靶基因网络 | miRNA target network | 在线绘制miRNA靶基因网络图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_miRNA_target_network_plot_197) |
| 相关系数网络图 | correlation network | 在线绘制相关系数网络图（correlation network） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_correlation_network_plot_199) |
| mantel相关性网络 | mantel correlation network | 在线绘制mantel相关性网络图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_mantel_correlation_network_plot_271) |
| 两列桑基图 | sankey colorbar | 在线绘制右侧为颜色渐变的两列桑基图（sankey diagram） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_two_columns_sankey_with_colorbar_280) |
| 边捆绑图 | edge bundle | 在线绘制edge bundle圈图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_hierarchical_edge_bundle_plot) |
| 带权重的桑基图 | weighted sankey diagram | 在线绘制带权重的桑基图（weighted sankey diagram） | [在线绘制](https://www.bioinformatics.com.cn/basic_weighted_sankey_diagram) |
| 冲积图，ceRNA | alluvial ceRNA | 免费在线绘制冲积图（alluvial plot） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_alluvial_plot_017) |

### 地图 (Maps) — 28 tools

**适用场景:** 用于地理空间数据可视化

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 湖南地图_疫情图 | Hunan map | 在线绘制中国湖南省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_hunan_heatmap_019) |
| 上海市地图，疫情图 | shanghai map | 在线绘制中国上海市地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_shanghai_heatmap_156) |
| 四川省地图，疫情图 | sichuan map | 在线绘制中国四川省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_sichuan_heatmap_157) |
| 江苏省地图 疫情图 | jiangsu map | 在线绘制中国江苏省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_jiangsu_heatmap_158) |
| 安徽省地图 疫情图 | anhui map | 在线绘制中国安徽省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_anhui_heatmap_159) |
| 世界地图 疫情图 | world heatmap | 免费在线绘制世界地图（疫情图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_world_heatmap_015) |
| 浙江省地图，疫情图 | zhejiang map | 在线绘制中国浙江省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_zhejiang_heatmap_160) |
| 广东省地图，疫情图 | guangdong map | 在线绘制中国广东省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_guangdong_heatmap_163) |
| 吉林省地图_疫情图 | jilin map | 在线绘制中国吉林省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_jilin_heatmap_164) |
| 陕西省地图_疫情图 | shaanxi map | 在线绘制中国陕西省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_shaanxi_heatmap_165) |
| 山西省地图，疫情图 | shanxi map | 在线绘制中国山西省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_shanxi_heatmap_166) |
| 福建省地图_疫情图 | fujian map | 在线绘制中国福建省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_fujian_heatmap_167) |
| 河北省地图_疫情图 | hebei map | 在线绘制中国河北省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_hebei_heatmap_168) |
| 湖北省地图，疫情图 | hubei map | 在线绘制中国湖北省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_hubei_heatmap_169) |
| 贵州省地图，疫情图 | guizhou map | 在线绘制中国贵州省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_guizhou_heatmap_170) |
| 河南省地图，疫情图 | henan map | 在线绘制中国河南省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_henan_heatmap_161) |
| 山东省地图，疫情图 | shandong map | 在线绘制中国山东省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_shandong_heatmap_162) |
| 甘肃省地图，疫情图 | gansu map | 在线绘制中国甘肃省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_gansu_heatmap_171) |
| 宁夏地图，疫情图 | ningxia map | 在线绘制中国宁夏回族自治区地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_ningxia_heatmap_172) |
| 广西地图，疫情图 | guangxi map | 在线绘制中国广西壮族自治区地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_guangxi_heatmap_176) |
| 江西省地图 | jiangxi map | 在线绘制中国江西省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_jiangxi_heatmap_192) |
| 带散点的世界地图 | world map distribution | 在线绘制带散点的世界地图（world map with scatter） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_world_map_with_scatter_points_plot_194) |
| 带散点的中国地图 | china map distribution | 在线绘制带散点的中国地图（china map with scatter） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_map_with_scatter_points_plot_195) |
| 饼图散点世界地图 | pie scatter world map | 在线绘制带饼图比例散点的世界地图（world map with pie scatter） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_world_map_with_pie_scatter_points_plot_203) |
| 饼图散点中国地图 | china map pie | 在线绘制带饼图比例散点的中国地图（china map with pie scatter） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_map_with_pie_scatter_points_plot_205) |
| 美国地图 | usa american map | 在线绘制带颜色梯度的美国地图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_usa_choropleth_map_255) |
| 辽宁省地图 | liaoning map | 在线绘制中国辽宁省地图（疫情图，热图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_liaoning_heatmap_177) |
| 中国地图，疫情图 | China map, epidemic heatmap | 免费在线绘制中国地图（疫情图） | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_china_heatmap_012) |

### 单细胞图 (Single Cell) — 2 tools

**适用场景:** 用于单细胞RNA-seq数据的可视化

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| 单细胞umap，tsne降维 | scRNA umap tsne | 在线绘制单细胞转录组UMAP，tsne降维图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_umap_tsne_dimensionality_reduction_by_scrnatoolvis_258) |
| 单细胞umap，tsne降维 | scRNA umap tsne dimplot | 使用seurat dimplot在线绘制单细胞转录组UMAP，tsne降维图 | [在线绘制](https://www.bioinformatics.com.cn/plot_basic_umap_tsne_dimensionality_reduction_by_seurat_dimplot_259) |

### 分析工具 (Analysis Tools) — 18 tools

**适用场景:** 差异分析、富集分析、特征选择等计算工具

| 中文名 | 英文关键词 | 说明 | 链接 |
|--------|-----------|------|------|
| GO_KEGG富集分析 | go kegg pathway enrichment | 在线GO，KEGG pathway富集分析 | [在线绘制](https://www.bioinformatics.com.cn/basic_local_go_pathway_enrichment_analysis_122) |
| miRanda_miRNA靶基因预测 | miRNA target prediction | miRanda在线预测miRNA-mRNA，miRNA-circRNA，miRNA-lncRNA结合 | [在线绘制](https://www.bioinformatics.com.cn/local_miranda_miRNA_target_prediction_120) |
| KEGG任意物种通路富集分析 | kegg pathway enrichment analysis | 在线KEGG数据库任意物种（鸟类，鱼类，昆虫，细菌，真菌，植物，病毒等）通路富集分析 | [在线绘制](https://www.bioinformatics.com.cn/basic_kegg_any_species_pathway_enrichment_analysis_235) |
| 同源基因 | homologene | 免费在线批量查询不同物种的同源基因 | [在线绘制](https://www.bioinformatics.com.cn/batch_homologous_gene_t009) |
| lasso cox回归模型 | lasso cox regression | 在线LASSO Cox回归模型进行特征基因筛选（glmnet R包） | [在线绘制](https://www.bioinformatics.com.cn/basic_lasso_cox_regression_gene_feature_selection_t021) |
| xgboost基因特征筛选 | xgboost feature selection | 在线xgboost机器学习算法进行特征基因筛选 | [在线绘制](https://www.bioinformatics.com.cn/basic_xgboost_gene_feature_selection_t020) |
| 富集峰注释 | peak annotation, chipseq, atac | 在线chipseq, atac-seq等基因组区域peak chipseeker注释 | [在线绘制](https://www.bioinformatics.com.cn/basic_chipseq_atacseq_peak_annotation_by_chipseeker_t017) |
| cibersort免疫浸润 | cibersort | 在线human mouse cibersort免疫浸润分析 | [在线绘制](https://www.bioinformatics.com.cn/basic_human_mouse_cibersort_analysis_t011) |
| 基因集变异分析 | gene set variation analysis | 在线基因集变异分析（GSVA） | [在线绘制](https://www.bioinformatics.com.cn/basic_gene_set_variation_analysis_by_gsva_131) |
| PPI网络图 | network graph | 在线绘制蛋白质-蛋白质相互作用网络（PPI network） | [在线绘制](https://www.bioinformatics.com.cn/basic_protein_protein_interaction_network_by_igraph_256) |
| TCGA泛癌配对box图 | TCGA pan-cancer paired box | 在线TCGA泛癌基因表达配对肿瘤vs正常box图 | [在线绘制](https://www.bioinformatics.com.cn/plot_tcgaplot_pan_cancer_gene_expression_paired_tumor_vs_normal_boxplot_301) |
| SVM-RFE特征选择 | svm-rfe featue selection | 在线SVM-RFE机器学习算法进行两组分类的特征筛选 | [在线绘制](https://www.bioinformatics.com.cn/plot_two_group_svm_rfe_gene_feature_selection_t027) |
| 非模式生物GO，KEGG富集分析 | non-model organism GO KEGG | 非模式生物在线GO，KEGG pathway富集分析 | [在线绘制](https://www.bioinformatics.com.cn/basic_go_pathway_enrichment_analysis_for_non_model_organism_278) |
| 随机森林生存特征提取 | random forest feature selection | 在线随机森林（random forest）进行特征基因筛选 | [在线绘制](https://www.bioinformatics.com.cn/basic_random_forest_gene_feature_selection_t022) |
| TCGA泛癌MSI | TCGA pan-cancer MSI | Error | [在线绘制](https://www.bioinformatics.com.cn/plot_tcgaplot_pan_cancer_gene_expression_and_msi_correlation_radar_chart_304) |
| TCGA泛癌表达 | TCGA expression | 在线TCGA泛癌基因表达肿瘤box图 | [在线绘制](https://www.bioinformatics.com.cn/plot_tcgaplot_pan_cancer_gene_expression_tumor_boxplot_302) |
| TCGA泛癌box图 | TCGA pan-cancer box | 在线TCGA泛癌基因表达肿瘤vs正常box图 | [在线绘制](https://www.bioinformatics.com.cn/plot_tcgaplot_pan_cancer_gene_expression_tumor_vs_normal_boxplot_300) |
| TCGA表达与TMB | tpm tmb correlation | 在线TCGA泛癌基因表达与肿瘤突变负荷（TMB）相关性雷达图 | [在线绘制](https://www.bioinformatics.com.cn/plot_tcgaplot_pan_cancer_gene_expression_and_tmb_correlation_radar_chart_303) |

## Key R Packages Used

| Package | Used For | Plot Examples |
|---------|----------|---------------|
| ggplot2 | General plotting | Most plots |
| clusterProfiler | GO/KEGG enrichment | Enrichment bubble, cnetplot |
| ComplexHeatmap | Advanced heatmaps | Clinical heatmap, annotated heatmap |
| EnhancedVolcano | Volcano plots | Labeled volcano |
| CMplot | SNP/Manhattan | Manhattan, SNP density |
| pathview | KEGG pathway coloring | Pathway with gene colors |
| Rcircos/circlize | Circos plots | Chromosome circos |
| survminer | Survival curves | KM survival |
| timeROC | Time-dependent ROC | TimeROC |
| maftools | MAF mutation | Oncoplot, MAF summary |
| ggbiplot | PCA biplot | PCA plot |
| Rtsne/umap | Dimensionality reduction | t-SNE, UMAP |
| Mfuzz | Time-series clustering | Soft clustering |
| GOplot | GO visualization | GO chord, GOcluster |
| LDheatmap | Linkage disequilibrium | LD heatmap |
| igraph | Network graphs | PPI network |
| corrplot | Correlation matrices | Correlation plot |
| cibersort | Immune deconvolution | Immune infiltration |
| ggpubr | Publication-ready plots | Box with stats |
| plotly | Interactive plots | Sunburst |

## Workflow Guides

### RNA-seq Differential Expression Workflow
1. DESeq2/limma差异分析 (tool) → 差异基因列表
2. 火山图 (volcano) → 展示差异倍数和显著性
3. 聚类热图 (heatmap) → 展示差异基因表达模式
4. GO/KEGG富集分析 (tool) → 功能注释
5. 富集气泡图/弦图 (enrichment) → 富集结果可视化

### Clinical Prognosis Workflow
1. 单因素/多因素Cox → 筛选预后基因
2. Lasso Cox回归 (tool) → 特征选择
3. 风险得分三联图 (clinical) → 风险模型展示
4. KM生存曲线 (clinical) → 生存分析
5. 时间依赖ROC (clinical) → 模型评估
6. 列线图 (clinical) → 临床预测模型

### Tumor Mutation Workflow
1. MAF突变汇总图 → 突变概览
2. MAF突变瀑布图 → 样本突变详情
3. 突变棒棒糖图 → 蛋白结构上的突变位置
4. SNP连锁不平衡 → LD分析
5. 曼哈顿图 → GWAS结果

### Single Cell Workflow
1. PCA降维 → 初始降维
2. UMAP/t-SNE → 细胞聚类可视化
3. 单细胞marker火山图 → marker基因筛选
4. 单细胞cluster火山图 → cluster间差异分析

### Enrichment Analysis Workflow
1. GO/KEGG富集分析 (tool) → 获取富集结果
2. 富集气泡图 → 富集程度和基因数
3. BP,CC,MF三合一 → GO三大类对比
4. GO弦图 → 基因-term关系
5. KEGG pathway (pathview) → 通路图上标注基因
6. GSEA → 基因集富集分析

## Data Format Requirements

Most tools accept tab-separated text files with:
- Row 1: Column headers
- Column 1: Gene/feature names
- Subsequent columns: Values

Specific requirements per plot type:
- **Heatmap:** Matrix (genes × samples), optional annotation columns
- **Volcano:** log2FoldChange, pvalue, gene names
- **Venn:** Gene lists (one per set)
- **Enrichment:** GO/KEGG results (term, pvalue, gene count)
- **Survival:** Time, event, group
- **PCA/UMAP:** Expression matrix
- **Network:** Edge list or adjacency matrix

## Platform URL Patterns

- Plot tools: `https://www.bioinformatics.com.cn/plot_basic_{name}_{number}`
- Analysis tools: `https://www.bioinformatics.com.cn/basic_{name}_{number}`
- Tool IDs: `_t0{xx}` suffix indicates analysis tool (not just plotting)
- Number suffix is unique per tool (e.g., _081, _046)

## Citation

Tao X, et al. SRplot: A free online platform for data visualization and graphing. PLoS One. 2023;18(11):e0294239.
