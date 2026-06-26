> 新版API V2若使用新版API V2想参考最佳实践请联系我们。

# 一、背景介绍
## 1.1 需求场景
随着数据智能技术的飞速发展，图像搜索技术正在越来越广泛地应用于各行各业。传统的图像搜索方法大多依赖于图像的元数据或标签，存在信息更新滞后、知识局限性、搜索精度不足等问题。如何有效提升图像搜索的精度和效率，成为了当前亟待解决的关键问题。
在此背景下，基于向量检索的图像搜索技术逐渐成为一种突破性解决方案。通过将图像转换为高维向量并在向量空间内计算相似度，能够大幅提升图像搜索的效率和精度，解决传统图像搜索方式中的局限。VikingDB作为一款支持大规模数据场景的向量数据库，具备出色的高性能、高可用性和大数据处理能力，凭借对字节千亿级检索需求的丰富经验，成为在大数据规模下图像搜索领域的领先产品。
VikingDB结合最先进的doubao多模态embedding模型，能够有效处理文本与图像的多模态数据，并通过高效的向量检索，帮助用户在电商平台、图库平台、内容审核、安防监控等场景中实现精准的图像搜索与分析。结合VikingDB的强大性能和doubao模型的多模态能力，企业能够构建更加智能、精准且高效的图像搜索解决方案，推动图像搜索技术在各行业、各业务场景中的广泛应用。

## 1.2 场景示例

1. **电商智能搜索**

以文搜图：用户输入“复古风格皮鞋”，即使商品标题中没有“复古”二字，系统也能根据图片语义匹配到类似款式的皮鞋。
以图搜图：用户上传一张明星穿的衣服照片，系统自动找到相似款或相同品牌的商品，助力精准购物推荐。

2. **社交媒体内容发现**

以文搜图：用户搜索“森林系的婚纱摄影”，系统理解“森林系”的概念，返回具有自然、绿意背景的婚纱照，而不是简单匹配“森林”或“婚纱”标签的图片。
以图搜图：用户上传一张自己喜欢的插画风格图片，系统推荐相似风格的插画作品或相关创作者，提高内容发现的精准度。

3. **版权保护与内容审核**

以文搜图：输入“梵高风格的夜景油画”，系统搜索数据库中具有相同绘画风格的图片，而不仅仅是“梵高”相关标签的作品。
以图搜图：上传一张艺术作品，系统能找到相似构图、风格甚至被修改过的版本，帮助发现潜在侵权行为。

4. **医疗影像智能检索** 

以文搜图：医生输入“CT显示肺部有磨玻璃影”，系统检索数据库中相似病变的医学影像，辅助医生参考类似病例。
以图搜图：医生上传患者的CT影像，系统从数据库中找到高度相似的病例，推荐相关诊断和治疗方案，提升诊疗效率。

## 1.3 方案思路

<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSI5MzVweCIgaGVpZ2h0PSI2NDFweCIgdmlld0JveD0iLTAuNSAtMC41IDkzNSA2NDEiPjxkZWZzLz48Zz48cmVjdCB4PSIyMjIuMzIiIHk9IjY3LjUiIHdpZHRoPSIxNTAuOTciIGhlaWdodD0iNzguMTMiIHJ4PSIxMS43MiIgcnk9IjExLjcyIiBmaWxsPSIjZmZmZmZmIiBzdHJva2U9IiMwMDAwMDAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBjZW50ZXI7IHdpZHRoOiAxNDlweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiAxMDdweDsgbWFyZ2luLWxlZnQ6IDIyM3B4OyI+PGRpdiBzdHlsZT0iYm94LXNpemluZzogYm9yZGVyLWJveDsgZm9udC1zaXplOiAwOyB0ZXh0LWFsaWduOiBjZW50ZXI7ICI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDE3cHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiAjMDAwMDAwOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm9ybWFsOyB3b3JkLXdyYXA6IG5vcm1hbDsgIj7pnIDopoHooqvmo4DntKLnmoQ8YnIgc3R5bGU9ImZvbnQtc2l6ZToxN3B4IiAvPuWbvueJhzwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHBhdGggZD0iTSAyMjIuMzIgMjcwLjEgTCAyMjIuMzIgMjE4LjAyIEMgMjIyLjMyIDIxMC44MyAyNTYuMTIgMjA1IDI5Ny44MSAyMDUgQyAzMzkuNSAyMDUgMzczLjI5IDIxMC44MyAzNzMuMjkgMjE4LjAyIEwgMzczLjI5IDI3MC4xIEMgMzczLjI5IDI3Ny4zIDMzOS41IDI4My4xMiAyOTcuODEgMjgzLjEyIEMgMjU2LjEyIDI4My4xMiAyMjIuMzIgMjc3LjMgMjIyLjMyIDI3MC4xIFoiIGZpbGw9IiNmZmZmZmYiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48cGF0aCBkPSJNIDIyMi4zMiAyMTguMDIgQyAyMjIuMzIgMjI1LjIxIDI1Ni4xMiAyMzEuMDQgMjk3LjgxIDIzMS4wNCBDIDMzOS41IDIzMS4wNCAzNzMuMjkgMjI1LjIxIDM3My4yOSAyMTguMDIiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBjZW50ZXI7IHdpZHRoOiAxNDlweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiAyNDRweDsgbWFyZ2luLWxlZnQ6IDIyM3B4OyI+PGRpdiBzdHlsZT0iYm94LXNpemluZzogYm9yZGVyLWJveDsgZm9udC1zaXplOiAwOyB0ZXh0LWFsaWduOiBjZW50ZXI7ICI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDE3cHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiAjMDAwMDAwOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm9ybWFsOyB3b3JkLXdyYXA6IG5vcm1hbDsgIj48YnIgc3R5bGU9ImZvbnQtc2l6ZToxN3B4IiAvPlRPU+ahtjwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHBhdGggZD0iTSAyOTcuODEgMTQ1LjYzIEwgMjk3LjgxIDE5OC42MyIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwMDAwIiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJzdHJva2UiLz48cGF0aCBkPSJNIDI5Ny44MSAyMDMuODggTCAyOTQuMzEgMTk2Ljg4IEwgMjk3LjgxIDE5OC42MyBMIDMwMS4zMSAxOTYuODggWiIgZmlsbD0iIzAwMDAwMCIgc3Ryb2tlPSIjMDAwMDAwIiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48cGF0aCBkPSJNIDUwNy40OCAzODAuMSBMIDUwNy40OCAzMjguMDIgQyA1MDcuNDggMzIwLjgzIDU0MS4yOCAzMTUgNTgyLjk3IDMxNSBDIDYyNC42NiAzMTUgNjU4LjQ1IDMyMC44MyA2NTguNDUgMzI4LjAyIEwgNjU4LjQ1IDM4MC4xIEMgNjU4LjQ1IDM4Ny4zIDYyNC42NiAzOTMuMTIgNTgyLjk3IDM5My4xMiBDIDU0MS4yOCAzOTMuMTIgNTA3LjQ4IDM4Ny4zIDUwNy40OCAzODAuMSBaIiBmaWxsPSIjZmZmZmZmIiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PHBhdGggZD0iTSA1MDcuNDggMzI4LjAyIEMgNTA3LjQ4IDMzNS4yMSA1NDEuMjggMzQxLjA0IDU4Mi45NyAzNDEuMDQgQyA2MjQuNjYgMzQxLjA0IDY1OC40NSAzMzUuMjEgNjU4LjQ1IDMyOC4wMiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwMDAwIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0wLjUgLTAuNSkiPjxmb3JlaWduT2JqZWN0IHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiIHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIj48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGNlbnRlcjsgd2lkdGg6IDE0OXB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDM1NHB4OyBtYXJnaW4tbGVmdDogNTA4cHg7Ij48ZGl2IHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDA7IHRleHQtYWxpZ246IGNlbnRlcjsgIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMTdweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6ICMwMDAwMDA7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3JtYWw7IHdvcmQtd3JhcDogbm9ybWFsOyAiPjxiciBzdHlsZT0iZm9udC1zaXplOjE3cHgiIC8+VmlraW5nREI8YnIgc3R5bGU9ImZvbnQtc2l6ZToxN3B4IiAvPuWQkemHj+W6kzwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHBhdGggZD0iTSAyOTcuODEgMjgzLjEzIEwgMjk3LjggMzU0LjEgTCA1MDEuMTIgMzU0LjA2IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9InN0cm9rZSIvPjxwYXRoIGQ9Ik0gNTA2LjM3IDM1NC4wNiBMIDQ5OS4zNyAzNTcuNTYgTCA1MDEuMTIgMzU0LjA2IEwgNDk5LjM3IDM1MC41NiBaIiBmaWxsPSIjMDAwMDAwIiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxwYXRoIGQ9Ik0gNTgyLjk3IDE0NS42MyBMIDU4Mi45NyAzMDguNjMiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0ic3Ryb2tlIi8+PHBhdGggZD0iTSA1ODIuOTcgMzEzLjg4IEwgNTc5LjQ3IDMwNi44OCBMIDU4Mi45NyAzMDguNjMgTCA1ODYuNDcgMzA2Ljg4IFoiIGZpbGw9IiMwMDAwMDAiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLW1pdGVybGltaXQ9IjEwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PHJlY3QgeD0iNTA3LjQ4IiB5PSI2Ny41IiB3aWR0aD0iMTUwLjk3IiBoZWlnaHQ9Ijc4LjEzIiByeD0iMTEuNzIiIHJ5PSIxMS43MiIgZmlsbD0iI2ZmZmZmZiIgc3Ryb2tlPSIjMDAwMDAwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyIgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgY2VudGVyOyB3aWR0aDogMTQ5cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogMTA3cHg7IG1hcmdpbi1sZWZ0OiA1MDhweDsiPjxkaXYgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMDsgdGV4dC1hbGlnbjogY2VudGVyOyAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxN3B4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogIzAwMDAwMDsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgd2hpdGUtc3BhY2U6IG5vcm1hbDsgd29yZC13cmFwOiBub3JtYWw7ICI+UXVlcnk8YnIgc3R5bGU9ImZvbnQtc2l6ZToxN3B4IiAvPuWbvi/mloc8L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjxyZWN0IHg9IjUwNy40OCIgeT0iNTM1IiB3aWR0aD0iMTUwLjk3IiBoZWlnaHQ9Ijc4LjEzIiByeD0iMTEuNzIiIHJ5PSIxMS43MiIgZmlsbD0iI2ZmZmZmZiIgc3Ryb2tlPSIjMDAwMDAwIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyIgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgY2VudGVyOyB3aWR0aDogMTQ5cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogNTc0cHg7IG1hcmdpbi1sZWZ0OiA1MDhweDsiPjxkaXYgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMDsgdGV4dC1hbGlnbjogY2VudGVyOyAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxN3B4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogIzAwMDAwMDsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgd2hpdGUtc3BhY2U6IG5vcm1hbDsgd29yZC13cmFwOiBub3JtYWw7ICI+5qOA57Si57uT5p6cPGJyIC8+5Zu+54mHPC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48cGF0aCBkPSJNIDU4Mi45NyAzOTMuMTMgTCA1ODIuOTcgNTI4LjY0IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9InN0cm9rZSIvPjxwYXRoIGQ9Ik0gNTgyLjk3IDUzMy44OSBMIDU3OS40NyA1MjYuODkgTCA1ODIuOTcgNTI4LjY0IEwgNTg2LjQ3IDUyNi44OSBaIiBmaWxsPSIjMDAwMDAwIiBzdHJva2U9IiMwMDAwMDAiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxyZWN0IHg9IjU0MS4wMyIgeT0iNSIgd2lkdGg9IjgzLjg3IiBoZWlnaHQ9IjMxLjI1IiBmaWxsPSJub25lIiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBjZW50ZXI7IHdpZHRoOiA4MnB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDIxcHg7IG1hcmdpbi1sZWZ0OiA1NDJweDsiPjxkaXYgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMDsgdGV4dC1hbGlnbjogY2VudGVyOyAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAyMHB4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogIzAwMDAwMDsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgd2hpdGUtc3BhY2U6IG5vcm1hbDsgd29yZC13cmFwOiBub3JtYWw7ICI+5Zu+54mH5qOA57SiPC9kaXY+PC9kaXY+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48cmVjdCB4PSIyNTUuODciIHk9IjUiIHdpZHRoPSI4My44NyIgaGVpZ2h0PSIzMS4yNSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyIgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgY2VudGVyOyB3aWR0aDogODJweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiAyMXB4OyBtYXJnaW4tbGVmdDogMjU3cHg7Ij48ZGl2IHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDA7IHRleHQtYWxpZ246IGNlbnRlcjsgIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMjBweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6ICMwMDAwMDA7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3JtYWw7IHdvcmQtd3JhcDogbm9ybWFsOyAiPuWbvueJh+WtmOWFpTwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHJlY3QgeD0iMiIgeT0iMjgzLjEzIiB3aWR0aD0iMzAwIiBoZWlnaHQ9IjcwIiBmaWxsPSJub25lIiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LXN0YXJ0OyB3aWR0aDogMjk4cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogMzE4cHg7IG1hcmdpbi1sZWZ0OiA0cHg7Ij48ZGl2IHN0eWxlPSJib3gtc2l6aW5nOiBib3JkZXItYm94OyBmb250LXNpemU6IDA7IHRleHQtYWxpZ246IGxlZnQ7ICI+PGRpdiBzdHlsZT0iZGlzcGxheTogaW5saW5lLWJsb2NrOyBmb250LXNpemU6IDE3cHg7IGZvbnQtZmFtaWx5OiBIZWx2ZXRpY2E7IGNvbG9yOiAjMDAwMDAwOyBsaW5lLWhlaWdodDogMS4yOyBwb2ludGVyLWV2ZW50czogYWxsOyB3aGl0ZS1zcGFjZTogbm9ybWFsOyB3b3JkLXdyYXA6IG5vcm1hbDsgIj4yLiDlsIZUT1PkuK3lm77niYfnmoTlnLDlnYDkvKDlhaVWaWtpbmdEQu+8jDxiciAvPsKgIMKgIOWbvueJh+S8muiiq+iHquWKqOWQkemHj+WMluWtmOWFpTwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHBhdGggZD0iTSA0NDIgNjM1IEwgNDQyIDUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMDAwMCIgc3Ryb2tlLXdpZHRoPSI2IiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHN0cm9rZS1kYXNoYXJyYXk9IjE4IDE4IiBwb2ludGVyLWV2ZW50cz0ic3Ryb2tlIi8+PHJlY3QgeD0iMjIiIHk9IjE2NSIgd2lkdGg9IjMwMCIgaGVpZ2h0PSIyMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJub25lIiBwb2ludGVyLWV2ZW50cz0iYWxsIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTAuNSAtMC41KSI+PGZvcmVpZ25PYmplY3Qgc3R5bGU9Im92ZXJmbG93OiB2aXNpYmxlOyB0ZXh0LWFsaWduOiBsZWZ0OyIgcG9pbnRlci1ldmVudHM9Im5vbmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkaXYgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHN0eWxlPSJkaXNwbGF5OiBmbGV4OyBhbGlnbi1pdGVtczogdW5zYWZlIGNlbnRlcjsganVzdGlmeS1jb250ZW50OiB1bnNhZmUgZmxleC1zdGFydDsgd2lkdGg6IDI5OHB4OyBoZWlnaHQ6IDFweDsgcGFkZGluZy10b3A6IDE3NXB4OyBtYXJnaW4tbGVmdDogMjRweDsiPjxkaXYgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMDsgdGV4dC1hbGlnbjogbGVmdDsgIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMTdweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6ICMwMDAwMDA7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3JtYWw7IHdvcmQtd3JhcDogbm9ybWFsOyAiPjEuIOWwhumcgOimgeiiq+ajgOe0oueahOWbvueJh+WtmOWFpVRPUzwvZGl2PjwvZGl2PjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PHJlY3QgeD0iNTkyIiB5PSIyMTUiIHdpZHRoPSIzMDAiIGhlaWdodD0iMjAiIGZpbGw9Im5vbmUiIHN0cm9rZT0ibm9uZSIgcG9pbnRlci1ldmVudHM9ImFsbCIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0wLjUgLTAuNSkiPjxmb3JlaWduT2JqZWN0IHN0eWxlPSJvdmVyZmxvdzogdmlzaWJsZTsgdGV4dC1hbGlnbjogbGVmdDsiIHBvaW50ZXItZXZlbnRzPSJub25lIiB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIj48ZGl2IHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIiBzdHlsZT0iZGlzcGxheTogZmxleDsgYWxpZ24taXRlbXM6IHVuc2FmZSBjZW50ZXI7IGp1c3RpZnktY29udGVudDogdW5zYWZlIGZsZXgtc3RhcnQ7IHdpZHRoOiAyOThweDsgaGVpZ2h0OiAxcHg7IHBhZGRpbmctdG9wOiAyMjVweDsgbWFyZ2luLWxlZnQ6IDU5NHB4OyI+PGRpdiBzdHlsZT0iYm94LXNpemluZzogYm9yZGVyLWJveDsgZm9udC1zaXplOiAwOyB0ZXh0LWFsaWduOiBsZWZ0OyAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IGlubGluZS1ibG9jazsgZm9udC1zaXplOiAxN3B4OyBmb250LWZhbWlseTogSGVsdmV0aWNhOyBjb2xvcjogIzAwMDAwMDsgbGluZS1oZWlnaHQ6IDEuMjsgcG9pbnRlci1ldmVudHM6IGFsbDsgd2hpdGUtc3BhY2U6IG5vcm1hbDsgd29yZC13cmFwOiBub3JtYWw7ICI+My4g5bCGUXVlcnnlm77miJbogIXmlofovpPlhaXvvIzov5vooYzmo4DntKI8L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjxyZWN0IHg9IjYwMiIgeT0iNDQ1IiB3aWR0aD0iMzMwIiBoZWlnaHQ9IjIwIiBmaWxsPSJub25lIiBzdHJva2U9Im5vbmUiIHBvaW50ZXItZXZlbnRzPSJhbGwiLz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMC41IC0wLjUpIj48Zm9yZWlnbk9iamVjdCBzdHlsZT0ib3ZlcmZsb3c6IHZpc2libGU7IHRleHQtYWxpZ246IGxlZnQ7IiBwb2ludGVyLWV2ZW50cz0ibm9uZSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PGRpdiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCIgc3R5bGU9ImRpc3BsYXk6IGZsZXg7IGFsaWduLWl0ZW1zOiB1bnNhZmUgY2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6IHVuc2FmZSBmbGV4LXN0YXJ0OyB3aWR0aDogMzI4cHg7IGhlaWdodDogMXB4OyBwYWRkaW5nLXRvcDogNDU1cHg7IG1hcmdpbi1sZWZ0OiA2MDRweDsiPjxkaXYgc3R5bGU9ImJveC1zaXppbmc6IGJvcmRlci1ib3g7IGZvbnQtc2l6ZTogMDsgdGV4dC1hbGlnbjogbGVmdDsgIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiBpbmxpbmUtYmxvY2s7IGZvbnQtc2l6ZTogMTdweDsgZm9udC1mYW1pbHk6IEhlbHZldGljYTsgY29sb3I6ICMwMDAwMDA7IGxpbmUtaGVpZ2h0OiAxLjI7IHBvaW50ZXItZXZlbnRzOiBhbGw7IHdoaXRlLXNwYWNlOiBub3JtYWw7IHdvcmQtd3JhcDogbm9ybWFsOyAiPjQuIFZpa2luZ0RC6L+U5Zue5LiOUXVlcnnljLnphY3nmoTnu5Pmnpzlm77niYc8L2Rpdj48L2Rpdj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48L3N2Zz4=" from="flow-chart" payload="{&quot;data&quot;:{&quot;mxGraphModel&quot;:{&quot;dx&quot;:&quot;2893&quot;,&quot;dy&quot;:&quot;1099&quot;,&quot;grid&quot;:&quot;1&quot;,&quot;gridSize&quot;:&quot;10&quot;,&quot;guides&quot;:&quot;1&quot;,&quot;tooltips&quot;:&quot;1&quot;,&quot;connect&quot;:&quot;1&quot;,&quot;arrows&quot;:&quot;1&quot;,&quot;fold&quot;:&quot;1&quot;,&quot;page&quot;:&quot;1&quot;,&quot;pageScale&quot;:&quot;1&quot;,&quot;pageWidth&quot;:&quot;827&quot;,&quot;pageHeight&quot;:&quot;1169&quot;},&quot;mxCellMap&quot;:{&quot;q67jwhF7&quot;:{&quot;id&quot;:&quot;q67jwhF7&quot;},&quot;Ebm49qT3&quot;:{&quot;id&quot;:&quot;Ebm49qT3&quot;,&quot;parent&quot;:&quot;q67jwhF7&quot;},&quot;R3qWkmGy&quot;:{&quot;id&quot;:&quot;R3qWkmGy&quot;,&quot;value&quot;:&quot;需要被检索的<br style=\&quot;font-size: 17px;\&quot;>图片&quot;,&quot;style&quot;:&quot;rounded=1;whiteSpace=wrap;html=1;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;RoundedRectangle&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;200.32258064516128&quot;,&quot;y&quot;:&quot;262.5&quot;,&quot;width&quot;:&quot;150.96774193548384&quot;,&quot;height&quot;:&quot;78.125&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;YUsQpteJ&quot;:{&quot;id&quot;:&quot;YUsQpteJ&quot;,&quot;value&quot;:&quot;<br style=\&quot;font-size: 17px;\&quot;>TOS桶&quot;,&quot;style&quot;:&quot;shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;Database&quot;,&quot;diagramCategory&quot;:&quot;Flowchart&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;200.32258064516128&quot;,&quot;y&quot;:&quot;400&quot;,&quot;width&quot;:&quot;150.96774193548384&quot;,&quot;height&quot;:&quot;78.125&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;PQQHcpVK&quot;:{&quot;id&quot;:&quot;PQQHcpVK&quot;,&quot;style&quot;:&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;source&quot;:&quot;R3qWkmGy&quot;,&quot;target&quot;:&quot;YUsQpteJ&quot;,&quot;edge&quot;:&quot;1&quot;,&quot;-0-mxGeometry&quot;:{&quot;relative&quot;:&quot;1&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;zZwnCPlL&quot;:{&quot;id&quot;:&quot;zZwnCPlL&quot;,&quot;value&quot;:&quot;<br style=\&quot;font-size: 17px;\&quot;>VikingDB<br style=\&quot;font-size: 17px;\&quot;>向量库&quot;,&quot;style&quot;:&quot;shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;Database&quot;,&quot;diagramCategory&quot;:&quot;Flowchart&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;485.48387096774184&quot;,&quot;y&quot;:&quot;510&quot;,&quot;width&quot;:&quot;150.96774193548384&quot;,&quot;height&quot;:&quot;78.125&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;t4C3Y5Du&quot;:{&quot;id&quot;:&quot;t4C3Y5Du&quot;,&quot;style&quot;:&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;fontSize=17;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=0;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;source&quot;:&quot;YUsQpteJ&quot;,&quot;target&quot;:&quot;zZwnCPlL&quot;,&quot;edge&quot;:&quot;1&quot;,&quot;-0-mxGeometry&quot;:{&quot;relative&quot;:&quot;1&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;uYfn2A25&quot;:{&quot;id&quot;:&quot;uYfn2A25&quot;,&quot;style&quot;:&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;entryPerimeter=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;source&quot;:&quot;K2CaMdn1&quot;,&quot;target&quot;:&quot;zZwnCPlL&quot;,&quot;edge&quot;:&quot;1&quot;,&quot;-0-mxGeometry&quot;:{&quot;relative&quot;:&quot;1&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;K2CaMdn1&quot;:{&quot;id&quot;:&quot;K2CaMdn1&quot;,&quot;value&quot;:&quot;Query<br style=\&quot;font-size: 17px;\&quot;>图/文&quot;,&quot;style&quot;:&quot;rounded=1;whiteSpace=wrap;html=1;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;RoundedRectangle&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;485.48387096774184&quot;,&quot;y&quot;:&quot;262.5&quot;,&quot;width&quot;:&quot;150.96774193548384&quot;,&quot;height&quot;:&quot;78.125&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;GoCViyzv&quot;:{&quot;id&quot;:&quot;GoCViyzv&quot;,&quot;value&quot;:&quot;检索结果<br />图片&quot;,&quot;style&quot;:&quot;rounded=1;whiteSpace=wrap;html=1;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;RoundedRectangle&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;485.48387096774184&quot;,&quot;y&quot;:&quot;730.005&quot;,&quot;width&quot;:&quot;150.96774193548384&quot;,&quot;height&quot;:&quot;78.125&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;cLU7o3eW&quot;:{&quot;id&quot;:&quot;cLU7o3eW&quot;,&quot;style&quot;:&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;source&quot;:&quot;zZwnCPlL&quot;,&quot;target&quot;:&quot;GoCViyzv&quot;,&quot;edge&quot;:&quot;1&quot;,&quot;-0-mxGeometry&quot;:{&quot;relative&quot;:&quot;1&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;Dv91CXLg&quot;:{&quot;id&quot;:&quot;Dv91CXLg&quot;,&quot;value&quot;:&quot;图片检索&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;dashed=1;fontSize=20;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;519.0322580645161&quot;,&quot;y&quot;:&quot;200&quot;,&quot;width&quot;:&quot;83.87096774193546&quot;,&quot;height&quot;:&quot;31.250000000000004&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;zkN8PrlQ&quot;:{&quot;id&quot;:&quot;zkN8PrlQ&quot;,&quot;value&quot;:&quot;图片存入&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;dashed=1;fontSize=20;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;233.87096774193546&quot;,&quot;y&quot;:&quot;200&quot;,&quot;width&quot;:&quot;83.87096774193546&quot;,&quot;height&quot;:&quot;31.250000000000004&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;AEaDUPoE&quot;:{&quot;id&quot;:&quot;AEaDUPoE&quot;,&quot;value&quot;:&quot;2. 将TOS中图片的地址传入VikingDB，<br />    图片会被自动向量化存入&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;-20&quot;,&quot;y&quot;:&quot;478.13&quot;,&quot;width&quot;:&quot;300&quot;,&quot;height&quot;:&quot;70&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;iJ9hlEsd&quot;:{&quot;id&quot;:&quot;iJ9hlEsd&quot;,&quot;value&quot;:&quot;&quot;,&quot;style&quot;:&quot;endArrow=none;dashed=1;html=1;fontSize=28;strokeWidth=6;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;edge&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;dashed&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;width&quot;:&quot;50&quot;,&quot;height&quot;:&quot;50&quot;,&quot;relative&quot;:&quot;1&quot;,&quot;as&quot;:&quot;geometry&quot;,&quot;-0-mxPoint&quot;:{&quot;x&quot;:&quot;420&quot;,&quot;y&quot;:&quot;830&quot;,&quot;as&quot;:&quot;sourcePoint&quot;},&quot;-1-mxPoint&quot;:{&quot;x&quot;:&quot;420&quot;,&quot;y&quot;:&quot;200&quot;,&quot;as&quot;:&quot;targetPoint&quot;}}},&quot;UF5CUtmZ&quot;:{&quot;id&quot;:&quot;UF5CUtmZ&quot;,&quot;value&quot;:&quot;1. 将需要被检索的图片存入TOS&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;y&quot;:&quot;360&quot;,&quot;width&quot;:&quot;300&quot;,&quot;height&quot;:&quot;20&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;wHATJdDT&quot;:{&quot;id&quot;:&quot;wHATJdDT&quot;,&quot;value&quot;:&quot;3. 将Query图或者文输入，进行检索&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;570&quot;,&quot;y&quot;:&quot;410&quot;,&quot;width&quot;:&quot;300&quot;,&quot;height&quot;:&quot;20&quot;,&quot;as&quot;:&quot;geometry&quot;}},&quot;wyjfzP0L&quot;:{&quot;id&quot;:&quot;wyjfzP0L&quot;,&quot;value&quot;:&quot;4. VikingDB返回与Query匹配的结果图片&quot;,&quot;style&quot;:&quot;text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=17;&quot;,&quot;parent&quot;:&quot;Ebm49qT3&quot;,&quot;vertex&quot;:&quot;1&quot;,&quot;diagramName&quot;:&quot;text&quot;,&quot;diagramCategory&quot;:&quot;general&quot;,&quot;-0-mxGeometry&quot;:{&quot;x&quot;:&quot;580&quot;,&quot;y&quot;:&quot;640&quot;,&quot;width&quot;:&quot;330&quot;,&quot;height&quot;:&quot;20&quot;,&quot;as&quot;:&quot;geometry&quot;}}},&quot;mxCellList&quot;:[&quot;q67jwhF7&quot;,&quot;Ebm49qT3&quot;,&quot;R3qWkmGy&quot;,&quot;YUsQpteJ&quot;,&quot;PQQHcpVK&quot;,&quot;zZwnCPlL&quot;,&quot;t4C3Y5Du&quot;,&quot;uYfn2A25&quot;,&quot;K2CaMdn1&quot;,&quot;GoCViyzv&quot;,&quot;cLU7o3eW&quot;,&quot;Dv91CXLg&quot;,&quot;zkN8PrlQ&quot;,&quot;AEaDUPoE&quot;,&quot;iJ9hlEsd&quot;,&quot;UF5CUtmZ&quot;,&quot;wHATJdDT&quot;,&quot;wyjfzP0L&quot;]},&quot;lastEditTime&quot;:0,&quot;snapshot&quot;:&quot;&quot;}" />



## 1.4 方案优势

1. **精准的视觉匹配**：借助深层次特征提取，能将风格、场景和对象相似的图片准确检索；
2. **超大规模高效检索**：针对十亿量级的图片，VikingDB向量数据库能极快完成相似度匹配，让检索效率成倍提升；
3. **跨模态搜索**：不仅能实时接收并索引新图片，还可结合文本信息进行搜索，方便快速定位和分析目标素材；


# 二、快速搭建
## 2.1 案例场景与数据
下面我们将使用VikingDB向量数据库进行以文搜图和以图搜图，即输入文本或图片，检索出对应的图片。本案例使用pic_search_1000_images.zip数据，其中包含1000张野生动物图片。
请下载该数据压缩包并解压<span style="color: #D83931">，解压后的图片文件夹需要和Python代码放在同一目录下。</span>
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/0566b538a47c4523923f1327f0a2d1a4~tplv-goo7wpa0wc-image.image" filename="pic_search_1000_images.zip" download>pic_search_1000_images.zip</a>
> 该数据抽样自 Sourav Banerjee 在 Kaggle 上发布的 *Animal Image Dataset*数据集，数据源为：https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals。


## 2.2 服务开通、密钥与环境准备
<span style="color: #D83931">请注意，以下每一步都是完成多模态检索的必要条件，请勿遗漏。</span>

1. VikingDB账号注册与服务开通：[注册账号及开通服务--向量数据库VikingDB-火山引擎](https://www.volcengine.com/docs/84313/1254444)；
2. TOS（对象存储Torch Object Storage）服务开通：[去开通](https://console.volcengine.com/tos/bucket/create)，开通后您可以把图片存在TOS桶中；
3. 授权 VikingDB 服务可以访问您的 TOS 权限：[去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)，授权后VikingDB就可以访问TOS中的图片；
4. 获取安全凭证Access Key ID（简称为AK）和Secret Access Key（简称为SK）：[Access Key(密钥)管理--API访问密钥(Access Key)-火山引擎](https://www.volcengine.com/docs/6291/65568)；
5. 推荐Python 3.7及以上；
6. 运行环境准备，在终端（Terminal）输入以下指令：

| **VikingDB SDK安装** | pip3 install --upgrade volcengine  | 用于使用VikingDB的服务 |
| --- | --- | --- |
| **TOS安装** | pip3 install --upgrade tos | 用于使用TOS服务 |
| **requests安装** | pip3 install --upgrade requests | HTTP请求库 |
| **aiohttp安装** | pip3 install --upgrade aiohttp | 异步HTTP通信框架 |
| **tqdm安装** | pip3 install --upgrade tqdm | 用于进度条显示 |

## 2.3 数据准备
### 2.3.1 创建TOS桶
网页操作和Python操作二选一即可，效果相同。

<div type="doc-tabs">
<div type="tab-item" title="网页操作" key="Y9Thpo8m4U">

此处创建一个TOS桶，此处桶的命名为"best-practice-pic-search-tos"。可以修改TOS桶名称，但是不建议修改，因为此处修改后，后面的代码全部都要修改才能正常运行。
> **TOS是什么？**
> 火山引擎对象存储 TOS（Torch Object Storage）是火山引擎提供的海量、安全、低成本、易用、高可靠、高可用的分布式云存储服务。您可以通过 RESTful API 接口、SDK 和工具等多种形式使用火山引擎 TOS。通过网络，您可以在任何应用、任何时间、任何地点管理和访问火山引擎 TOS 上的数据。
> 更多关于TOS的信息可以查阅[TOS帮助文档](https://www.volcengine.com/docs/6349)。


1. 在火山引擎官网打开对象储存（TOS），点击”桶列表“

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/291b338880cd4024a32365a1e124496d~tplv-goo7wpa0wc-image.image)

2. 点击”创建桶“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6700e9de2e504858b697ce3d024cf096~tplv-goo7wpa0wc-image.image)

3. 给TOS桶命名、选择区域、桶策略，然后点击确定，就能看见列表里有

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/cd413fb2d64641a1bf5b158d955ef05c~tplv-goo7wpa0wc-image.image)
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f4d763e2af2d42e0b082bc3bc385d59e~tplv-goo7wpa0wc-image.image)
至此，您的TOS桶就创建完毕了。

</div>
<div type="tab-item" title="Python操作" key="A26bg2FBOZ">

此处初始化TOS服务的的Python SDK，然后创建一个TOS桶，此处桶的命名为"best-practice-pic-search-tos"。可以修改TOS桶名称。
> **TOS是什么？**
> 火山引擎对象存储 TOS（Torch Object Storage）是火山引擎提供的海量、安全、低成本、易用、高可靠、高可用的分布式云存储服务。您可以通过 RESTful API 接口、SDK 和工具等多种形式使用火山引擎 TOS。通过网络，您可以在任何应用、任何时间、任何地点管理和访问火山引擎 TOS 上的数据。
> 更多关于TOS的信息可以查阅[TOS帮助文档](https://www.volcengine.com/docs/6349)。

<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
import tos # pip3 install --upgrade tos

# 初始化tos客户端
ak = "*"  # 双引号内填入您的Access Key ID（简称为AK）
sk = "*"  # 双引号内填入您的Secret Access Key（简称为SK）
endpoint = "tos-cn-beijing.volces.com" # 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com
region = "cn-beijing" # region 填写 cn-beijing。
client = tos.TosClientV2(ak, sk, endpoint, region)


# 创建TOS桶
bucket_name = "best-practice-pic-search-tos" # TOS桶名称
try:
    # 创建 TosClientV2 对象，对桶和对象的操作都通过 TosClientV2 实现
    client = tos.TosClientV2(ak, sk, endpoint, region)
    # 在创建存储空间时指定桶存储类型，可设置可选参数storage_class
    # 在创建存储空间时指定桶访问权限，可设置可选参数acl
    # 在创建存储空间时指定桶指定AZ属性, 可设置可选参数az_redundancy
    # 以配置桶为标准存储类型, 访问权限为私有, 数据容灾为3az存储为例
    client.create_bucket(bucket_name, acl=tos.ACLType.ACL_Private,
                         storage_class=tos.StorageClassType.Storage_Class_Standard,
                         az_redundancy=tos.AzRedundancyType.Az_Redundancy_Multi_Az)
except tos.exceptions.TosClientError as e:
    # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
    print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
except tos.exceptions.TosServerError as e:
    # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
    print('fail with server error, code: {}'.format(e.code))
    # request id 可定位具体问题，强烈建议日志中保存
    print('error with request id: {}'.format(e.request_id))
    print('error with message: {}'.format(e.message))
    print('error with http code: {}'.format(e.status_code))
    print('error with ec: {}'.format(e.ec))
    print('error with request url: {}'.format(e.request_url))
except Exception as e:
    print('fail with unknown error: {}'.format(e))
```

至此，您的TOS桶就创建完毕了。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f4d763e2af2d42e0b082bc3bc385d59e~tplv-goo7wpa0wc-image.image)


</div>
</div>


### 2.3.2 上传图片文件夹
网页操作和Python操作二选一即可，效果相同。

<div type="doc-tabs">
<div type="tab-item" title="网页操作" key="yu6g2IFGHc">

此处将图片文件夹pic_search_1000_images上传至上一步创建的TOS桶中。

1. 点击刚才创建的“best-practice-pic-search-tos”桶；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b5f52630001548b8bafc8114d9d256e2~tplv-goo7wpa0wc-image.image)

2. 点击”上传文件“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ae7e81b1f723436f942183d573e31aae~tplv-goo7wpa0wc-image.image)

3. 拖拽pic_search_1000_images文件夹拖拽进去，然后点击”上传“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/04de32f07f2547dfba020a443b45d4c0~tplv-goo7wpa0wc-image.image)

4. 稍作等待，图片就会上传完成，任务状态会显示”执行成功“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e3f871c3cef34b8591c97db5178e5c9b~tplv-goo7wpa0wc-image.image)
至此，上传图片到TOS桶中这一步骤就完成了。

</div>
<div type="tab-item" title="Python操作" key="QLBNPXMPhw">

此处将图片文件夹pic_search_1000_images上传至上一步创建的TOS桶中，所以<span style="color: #D83931">需要您将pic_search_1000_images文件夹和该Python代码放在同一目录下</span>。
<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
import tos # pip3 install --upgrade tos
import os
from tqdm import tqdm # pip3 install --upgrade tqdm 用于进度条显示

# 初始化tos客户端
ak = "*"  # 双引号内填入您的Access Key ID（简称为AK）
sk = "*"  # 双引号内填入您的Secret Access Key（简称为SK）
endpoint = "tos-cn-beijing.volces.com" # 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com
region = "cn-beijing" # region 填写 cn-beijing。
client = tos.TosClientV2(ak, sk, endpoint, region)

# 开始上传图片
bucket_name = "best-practice-pic-search-tos" # tos桶名称
file_dir = "pic_search_1000_images" # 本地文件的当前路径
try:
    # 创建 TosClientV2 对象，对桶和对象的操作都通过 TosClientV2 实现
    client = tos.TosClientV2(ak, sk, endpoint, region)

    # 递归获取所有文件的路径
    def get_all_files(root_dir):
        file_paths = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths

    all_files = get_all_files(file_dir)

    # 使用 tqdm 显示进度条
    for file_path in tqdm(all_files, desc="图片上传进度", unit="file"):
        client.put_object_from_file(bucket_name, file_path, file_path)

except tos.exceptions.TosClientError as e:
    # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
    print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
except tos.exceptions.TosServerError as e:
    # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
    print('fail with server error, code: {}'.format(e.code))
    print('error with request id: {}'.format(e.request_id))
    print('error with message: {}'.format(e.message))
    print('error with http code: {}'.format(e.status_code))
    print('error with ec: {}'.format(e.ec))
    print('error with request url: {}'.format(e.request_url))
except Exception as e:
    print('fail with unknown error: {}'.format(e))
```


</div>
</div>

### 2.3.3 导出TOS中图片的路径
该步骤只能使用代码完成。
使用VikingDB进行图片检索时，并不是将图片本身直接传入VikingDB，而是将TOS桶中图片的地址存入VikingDB。VikingDB会访问图片的TOS地址，自动将图片向量化，并把向量也存入VikingDB。
以下代码作用就是导出您存在TOS中图片的tos地址，并保存为一个jsonl和一个json文件。
<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
import tos # pip3 install --upgrade tos
import json
import os


# 初始化tos客户端
ak = "*"
sk = "*"
endpoint = "tos-cn-beijing.volces.com" # 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com
region = "cn-beijing" # region 填写 cn-beijing。
client = tos.TosClientV2(ak, sk, endpoint, region)


bucket_name = "animal-zz" # TOS桶名称
prefix = "pic_search_1000_images/" # 前缀,即你的图片文件夹名称加一个斜杠，如果上传的是图片本身而不是文件夹，则prefix为空即可prefix = ""
output_file = "pic_search_copy.jsonl"  # 输出文件

# 新增：定义jsonl和json文件夹路径
jsonl_folder = "jsonl"
json_diku_folder = "json"

# 确保文件夹存在
os.makedirs(jsonl_folder, exist_ok=True)
os.makedirs(json_diku_folder, exist_ok=True)

# 修改：直接在jsonl文件夹中生成输出文件路径
jsonl_output_path = os.path.join(jsonl_folder, output_file)


def convert_jsonl_to_json(input_dir, output_dir):
    # 获取所有.jsonl文件
    jsonl_files = [f for f in os.listdir(input_dir) if f.endswith('.jsonl')]
    
    for jsonl_file in jsonl_files:
        input_path = os.path.join(input_dir, jsonl_file)
        # 生成输出文件名（将.jsonl替换为.json）
        json_file = jsonl_file.replace('.jsonl', '.json')
        output_path = os.path.join(output_dir, json_file)
        
        # 读取.jsonl文件并转换
        data = []
        with open(input_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                data.append(json.loads(line))
        
        # 写入.json文件
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)
        
        print(f"已转换 {jsonl_file} 到 {json_file}")

try:
    # 创建 TosClientV2 对象，对桶和对象的操作都通过 TosClientV2 实现
    client = tos.TosClientV2(ak, sk, endpoint, region)


    truncated = True
    continuation_token = ''
    image_id = 1  # 初始 id


    # 修改：直接在jsonl文件夹中创建和写入文件
    with open(jsonl_output_path, "w", encoding="utf-8") as f:
        while truncated:
            result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token)
            for item in result.contents:
                record = {
                    "image_id": str(image_id),
                    "animal_image": f"tos://{bucket_name}/{item.key}" # 图片路径格式为：【tos://{bucket}/{object_key}】，不包含【】，可用于向量化
                }
                # 写入一行 JSON
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                image_id += 1


            truncated = result.is_truncated
            continuation_token = result.next_continuation_token
    
    # 新增：转换jsonl文件为json文件并保存到json_diku文件夹
    convert_jsonl_to_json(jsonl_folder, json_diku_folder)
    print("所有文件转换完成！")


except tos.exceptions.TosClientError as e:
    # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
    print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
except tos.exceptions.TosServerError as e:
    # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
    print('fail with server error, code: {}'.format(e.code))
    print('error with request id: {}'.format(e.request_id))
    print('error with message: {}'.format(e.message))
    print('error with http code: {}'.format(e.status_code))
    print('error with ec: {}'.format(e.ec))
    print('error with request url: {}'.format(e.request_url))
except Exception as e:
    print('fail with unknown error: {}'.format(e))
```

代码运行完成后，会在代码所在目录下生成一个名为best_practice_pic_search_1000_image.jsonl的文件。
<a href="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/27ea76094a004065b5be318e7e6d0975~tplv-goo7wpa0wc-image.image" filename="best_practice_pic_search_1000_image.jsonl" download>best_practice_pic_search_1000_image.jsonl</a>
文件中存有1000条json，每一条json包含图片的id（"image_id"）和图片的tos地址（"animal_image"），tos地址会在后续步骤被传入VikingDB，json具体形式如下：
```Python
{"image_id": "1", "animal_image": "tos://best-practice-pic-search-tos/pic_search_1000_images/0009fc27d9.jpg"}
```


## 2.4 字段配置与创建VikingDB数据集
网页操作和Python操作二选一即可，效果相同。

<div type="doc-tabs">
<div type="tab-item" title="网页操作" key="eo1GaQdOBt">

此处在VikingDB中创建数据集（Collection）并配置字段，前面的图片tos地址就会被存在这个即将被创建的数据集中。
> **什么是字段？**

> * **字段定义**：字段（fields）是数据表中的基本单位，每个字段存储特定类型的数据，比如“姓名”字段存储人的名字，“年龄”字段存储数字信息。
> * **字段名**：下方代码的字段名（"field_name"）中，"image_id"字段用于储存图片的id，"animal_image"字段就储存图片的tos地址。
> * **字段类型**：不同字段可以配置不同的字段类型（"field_type"），比如"image_id"字段的类型是"int64"，也就是64 位整数**，**"animal_image"字段的类型是"image"，也就是他存入的是图片（TOS地址）。
1. 在VikingDB页面点击”创建数据集“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/32507c9f6b78400e848397bc5954bb56~tplv-goo7wpa0wc-image.image)


2. 选择”从向量化开始“，点击”开始创建“；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/10dd419184d24d32953fa8b85f22c498~tplv-goo7wpa0wc-image.image)


3. 设置数据集名称为”best_practice_pic_search“；选择使用场景为“图像”，选择向量化模型为“Doubao-embedding-vision250615”；选择向量维度为2048维；


![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/599e8646a3b4465db8404d377fc987ee~tplv-goo7wpa0wc-image.image)

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9e32afee8d8043b3bc79f48a516c7af3~tplv-goo7wpa0wc-image.image)


4. 配置向量文本字段名称为other_text，图片向量化字段名称为animal_image；其他字段名为image_id，类型int64；选择“从 string/int64 字段选择”，选择image_id；最后点击“创建数据集”；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6b971ec3065c43e9befd4076c0c929a8~tplv-goo7wpa0wc-image.image)

5. 此后您就能在数据集页面看到刚刚创建完成的”best_practice_pic_search“数据集；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/48d714a4e925441aa09b2d41dfaf408f~tplv-goo7wpa0wc-image.image)


</div>
<div type="tab-item" title="Python操作" key="CquVR12RpH">

此处代码用于配置字段，然后在VikingDB中创建数据集（Collection），前面的图片tos地址就会被存在这个即将被创建的数据集中。
> **什么是字段？**

> * **字段定义**：字段（fields）是数据表中的基本单位，每个字段存储特定类型的数据，比如“姓名”字段存储人的名字，“年龄”字段存储数字信息。
> * **字段名**：下方代码的字段名（"field_name"）中，"image_id"字段用于储存图片的id，"animal_image"字段就储存图片的tos地址。
> * **字段类型**：不同字段可以配置不同的字段类型（"field_type"），比如"image_id"字段的类型是"int64"，也就是64 位整数**，**"animal_image"字段的类型是"image"，也就是他存入的是图片（TOS地址）。

<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
import os
import datetime
import hashlib
import hmac
from urllib.parse import quote


import requests, json


def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                        query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")


def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class ClientForConsoleApi:
    def __init__(self, ak, sk, host, region):
        self.ak = ak
        self.sk = sk
        self.host = host
        self.region = region
        self.service_code = "vikingdb"
        self.version = "2025-06-09"


    def request(self, method, action, body, query=None, header=None):
        if query is None:
            query = {}
        if header is None:
            header = {}
        credential = {
            "access_key_id": self.ak,
            "secret_access_key": self.sk,
            "service": self.service_code,
            "region": self.region,
        }
        request_param = {
            "body": json.dumps(body),
            "host": self.host,
            "path": "/",
            "method": method,
            "content_type": 'application/json',
            "date": datetime.datetime.utcnow(),
            "query": {"Action": action, "Version": self.version, **query},
        }
        if body is None:
            request_param["body"] = ""
        x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
        short_x_date = x_date[:8]
        x_content_sha256 = hash_sha256(request_param["body"])
        sign_result = {
            "Host": request_param["host"],
            "X-Content-Sha256": x_content_sha256,
            "X-Date": x_date,
            "Content-Type": request_param["content_type"],
        }
        signed_headers_str = ";".join(
            ["content-type", "host", "x-content-sha256", "x-date"]
        )
        canonical_request_str = "\n".join(
            [request_param["method"].upper(),
             request_param["path"],
             norm_query(request_param["query"]),
             "\n".join(
                 [
                     "content-type:" + request_param["content_type"],
                     "host:" + request_param["host"],
                     "x-content-sha256:" + x_content_sha256,
                     "x-date:" + x_date,
                 ]
             ),
             "",
             signed_headers_str,
             x_content_sha256,
             ]
        )


        hashed_canonical_request = hash_sha256(canonical_request_str)
        credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
        string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])


        k_date = hmac_sha256(credential["secret_access_key"].encode("utf-8"), short_x_date)
        k_region = hmac_sha256(k_date, credential["region"])
        k_service = hmac_sha256(k_region, credential["service"])
        k_signing = hmac_sha256(k_service, "request")
        signature = hmac_sha256(k_signing, string_to_sign).hex()


        sign_result["Authorization"] = "HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}".format(
            credential["access_key_id"] + "/" + credential_scope,
            signed_headers_str,
            signature,
        )
        header = {**header, **sign_result}
        r = requests.request(method=method,
                             url="https://{}{}".format(request_param["host"], request_param["path"]),
                             headers=header,
                             params=request_param["query"],
                             data=request_param["body"],
                             )
        return r.status_code, r.headers, r.json()


if __name__ == '__main__':
    client = ClientForConsoleApi(
        ak = "*",#替换为您的ak
        sk ="*" ,#替换为您的sk
        host="vikingdb.cn-beijing.volcengineapi.com", #替换为您所在地区的域名
        region="cn-beijing"
    )
    http_code, _, result_json = client.request(
        method="POST",
        action="CreateVikingdbCollection",#创建
        body={
            "ProjectName": "default",#所在项目名称
            "CollectionName": "best_practice_pic_search",# 数据集名称
            "Description": "用于展示VikingDB的文搜图、图搜图能力",
            "Fields": [#定义声明每个字段
                {"FieldName": "image_id", "FieldType": "int64", "IsPrimaryKey": True},
                {"FieldName": "other_text", "FieldType": "text", },
                {"FieldName": "animal_image", "FieldType": "image", },
            ],
            "Vectorize": {
                "Dense": {
                    "ModelName": "doubao-embedding-vision",
                    "ModelVersion": "250615",
                    "TextField": "other_text",
                    "ImageField": "animal_image",
                    "Dimension": 2048,
                },
            }
        }
    )
    print("req http status code: ", http_code)
    print("req result: \n", result_json)
```


数据集创建成功后，VikingDB网页端数据集页面就可以看见该数据集。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7b0575996bcb47fd9f6c52ae98c30e38~tplv-goo7wpa0wc-image.image)


</div>
</div>

## 2.5 导入图片TOS地址到VikingDB的数据集
该步骤可以通过代码或本地完成。脚本与接口参考[数据面API调用流程](/c8p1dfoq/y0zjvsh5)[数据写入-UpsertData](/c8p1dfoq/7ytrusv1)
此处代码将best_practice_pic_search_1000_image.jsonl中的图片tos地址上传给best_practice_pic_search数据集中的"animal_image"字段。
TOS地址传入VikingDB的同时，其对应的图片会被自动向量化（Embedding），这样后面就可以进行向量相似度检索。这里向量化的速率是有一定限制的，每秒钟15张图。
<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
"""
pip3 install volcengine
"""
import os
from volcengine.auth.SignerV4 import SignerV4
from volcengine.Credentials import Credentials
from volcengine.base.Request import Request
import requests, json
# 举例：从 JSONL 文件逐条导入
import time
import json
class ClientForDataApi:
    def __init__(self, ak, sk, host):
        self.ak = ak
        self.sk = sk
        self.host = host



    def prepare_request(self, method, path, params=None, data=None):
        r = Request()
        r.set_shema("https")
        r.set_method(method)
        r.set_connection_timeout(10)
        r.set_socket_timeout(10)
        mheaders = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Host': self.host,
        }
        r.set_headers(mheaders)
        if params:
            r.set_query(params)
        r.set_host(self.host)
        r.set_path(path)
        if data is not None:
            r.set_body(json.dumps(data))
        credentials = Credentials(self.ak, self.sk, 'vikingdb', 'cn-beijing')
        SignerV4.sign(r, credentials)
        return r
        
    def do_req(self, req_method, req_path, req_params, req_body):
        req = self.prepare_request(method=req_method, path=req_path, params=req_params, data=req_body)
        return requests.request(method=req.method, url="http://{}{}".format(self.host, req.path),
                                  headers=req.headers, data=req.body, timeout=10000)
                                  
if __name__ == '__main__':
    client = ClientForDataApi(
        ak = "*",  # your ak
        sk = "*",  # your sk
        host = "api-vikingdb.vikingdb.cn-beijing.volces.com",
    )



    req_path = "/api/vikingdb/data/upsert"
    req_method = "POST"
    collection_name = "best_practice_pic_search"
    jsonl_path = "/Users/bytedance/workspace/video/animal.jsonl"#替换为你导出的TOS地址的路径
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            obj = json.loads(line)
            # 按你的字段构造单条 data
            one = {
                "image_id": obj["image_id"],
                "animal_image": {"value": obj["animal_image"]},  # 若服务端字段是对象需 value，若是字符串就直接传字符串
            }
            req_body = {
                "collection_name": collection_name,
                "data": [one],  # 单条
            }
            resp = client.do_req(req_method=req_method, req_path=req_path, req_params=None, req_body=req_body)
            print(f"[{idx}] status={resp.status_code} body={resp.text}")
            # 可选：限速避免触发 QPS 限制
            # time.sleep(0.01)
```

上传数据成功，**等待一段时间同步后**，在VikingDB向量数据库网页端-数据集页面，best_practice_pic_search数据集后方就可以看见数据量更新（该数据量是近似准确的）。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1dc0b65c04714aa689e742bd3808ab84~tplv-goo7wpa0wc-image.image)

## 2.6 创建索引
网页操作和Python操作二选一即可，效果相同。

<div type="doc-tabs">
<div type="tab-item" title="网页操作" key="LJyAzLuYGV">

此处为刚才的数据创建一个名为best_practice_pic_search_index的索引。
索引是对数据中某些字段的快速查找结构，VikingDB 索引支持对向量、标量的混合搜索需求。
> **向量索引参数说明：**

> * **distance**：指衡量向量之间距离（相似度）的算法，可以选择IP（计算向量内积，内积越大向，量相似度越高）、L2（计算向量之间的欧氏距离，欧氏距离越小，向量相似度越高）、COSINE（计算向量之间的余弦相似度，余弦相似度越大，向量相似度越高）.
> * **index_type**：向量索引类型，可以选择的类型有HNSW、HNSW_HYBRID、FLAT、IVF、DISKANN。本案例中选择HNSW算法，HNSW通过构建多层网络减少搜索过程中需要访问的节点数量，实现快速高效地搜索最近邻，适合对搜索效率要求较高的场景。
> * **quant**：量化方式，指索引中对向量的压缩方式，可以降低向量间相似性计算的复杂度，可选类型有Int8、Float、Fix16、PQ。本案例中选择Float，也就是不对向量压缩，保留向量全部精度。
> * **cpu_quota**：指索引检索消耗的 CPU 配额，1CPU 核约为 100QPS，取值范围是2到10240。本案例中使用2个CPU配额。
> * **description**：对索引的描述。
1. 找到刚才创建的best_practice_pic_search数据集，点击其右侧的“创建索引”；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3f8008b2de534ceda05b346b18730fa3~tplv-goo7wpa0wc-image.image)

2. 配置索引，设置索引名称为“best_practice_pic_search_index”，填写索引描述（非必填），选择数据集为best_practice_pic_search，选择CPU配额为1CU，选择索引分片方式为“自动化分片”，选择索引类型为“内存索引”，选择索引算法为“HNSW”，选择距离类型为“COSINE”，选择量化方式为“Int8”，点击“提交”；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4b9af9d936bd471289b9d905be9ceb48~tplv-goo7wpa0wc-image.image)

3. 操作完成后，就能在索引页面看到您刚才创建的索引best_practice_pic_search_index；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a74111d6ff82469e9d208825e0044938~tplv-goo7wpa0wc-image.image)

4. 稍作等待后，索引状态就会变成“已就绪”，此后就可以进行检索了；

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f71c7d190969404f839f98d113b80f4a~tplv-goo7wpa0wc-image.image)


</div>
<div type="tab-item" title="Python操作" key="dKRyBeokbL">

此处代码为刚才的数据创建一个名为best_practice_pic_search_index的索引。索引是对数据中某些字段的快速查找结构，VikingDB 索引支持对向量、标量的混合搜索需求。
> **向量索引参数说明：**

> * **distance**：指衡量向量之间距离（相似度）的算法，可以选择IP（计算向量内积，内积越大向，量相似度越高）、L2（计算向量之间的欧氏距离，欧氏距离越小，向量相似度越高）、COSINE（计算向量之间的余弦相似度，余弦相似度越大，向量相似度越高）.
> * **index_type**：向量索引类型，可以选择的类型有HNSW、HNSW_HYBRID、FLAT、IVF、DISKANN。本案例中选择HNSW算法，HNSW通过构建多层网络减少搜索过程中需要访问的节点数量，实现快速高效地搜索最近邻，适合对搜索效率要求较高的场景。
> * **quant**：量化方式，指索引中对向量的压缩方式，可以降低向量间相似性计算的复杂度，可选类型有Int8、Float、Fix16、PQ。本案例中选择Float，也就是不对向量压缩，保留向量全部精度。
> * **cpu_quota**：指索引检索消耗的 CPU 配额，1CPU 核约为 100QPS，取值范围是2到10240。
> * **description**：对索引的描述。

<span style="color: #D83931">需要您在代码开头填入您的ak和sk。</span>
```Python
import os
import datetime
import hashlib
import hmac
from urllib.parse import quote


import requests, json


def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                        query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")


def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class ClientForConsoleApi:
    def __init__(self, ak, sk, host, region):
        self.ak = ak
        self.sk = sk
        self.host = host
        self.region = region
        self.service_code = "vikingdb"
        self.version = "2025-06-09"


    def request(self, method, action, body, query=None, header=None):
        if query is None:
            query = {}
        if header is None:
            header = {}
        credential = {
            "access_key_id": self.ak,
            "secret_access_key": self.sk,
            "service": self.service_code,
            "region": self.region,
        }
        request_param = {
            "body": json.dumps(body),
            "host": self.host,
            "path": "/",
            "method": method,
            "content_type": 'application/json',
            "date": datetime.datetime.utcnow(),
            "query": {"Action": action, "Version": self.version, **query},
        }
        if body is None:
            request_param["body"] = ""
        x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
        short_x_date = x_date[:8]
        x_content_sha256 = hash_sha256(request_param["body"])
        sign_result = {
            "Host": request_param["host"],
            "X-Content-Sha256": x_content_sha256,
            "X-Date": x_date,
            "Content-Type": request_param["content_type"],
        }
        signed_headers_str = ";".join(
            ["content-type", "host", "x-content-sha256", "x-date"]
        )
        canonical_request_str = "\n".join(
            [request_param["method"].upper(),
             request_param["path"],
             norm_query(request_param["query"]),
             "\n".join(
                 [
                     "content-type:" + request_param["content_type"],
                     "host:" + request_param["host"],
                     "x-content-sha256:" + x_content_sha256,
                     "x-date:" + x_date,
                 ]
             ),
             "",
             signed_headers_str,
             x_content_sha256,
             ]
        )


        hashed_canonical_request = hash_sha256(canonical_request_str)
        credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
        string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])


        k_date = hmac_sha256(credential["secret_access_key"].encode("utf-8"), short_x_date)
        k_region = hmac_sha256(k_date, credential["region"])
        k_service = hmac_sha256(k_region, credential["service"])
        k_signing = hmac_sha256(k_service, "request")
        signature = hmac_sha256(k_signing, string_to_sign).hex()


        sign_result["Authorization"] = "HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}".format(
            credential["access_key_id"] + "/" + credential_scope,
            signed_headers_str,
            signature,
        )
        header = {**header, **sign_result}
        r = requests.request(method=method,
                             url="https://{}{}".format(request_param["host"], request_param["path"]),
                             headers=header,
                             params=request_param["query"],
                             data=request_param["body"],
                             )
        return r.status_code, r.headers, r.json()


if __name__ == '__main__':
    client = ClientForConsoleApi(
        ak = "*",#替换为您的ak
        sk ="*" ,#替换为您的sk
        host="vikingdb.cn-beijing.volcengineapi.com", #替换为您所在地区的域名
        region="cn-beijing"
    )
    http_code, _, result_json = client.request(
        method="POST",
        action="CreateVikingdbIndex",#action替换为当前操作
        body={
        "CollectionName": "best_practice_pic_search",
        "IndexName": "best_practice_pic_search_index",
        "cpu_quota":1,
        "Description": "test create index",
        "Vector_index": {
            "Index_type": "hnsw",
            "Distance": "cosine",
            "quant": "int8",
            },
        }    
    )
    print("req http status code: ", http_code)
    print("req result: \n", result_json)
```


代码运行成功后进入VikingDB网页端的索引页面，就可以看见索引best_practice_pic_search_index。一般刚创建完时，其其执行状态是”初始化中“，稍作等待后刷新页面，状态就会变为”已就绪“。接下来就可以进行图片检索了。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/941fb1fcabe042bf858e7ad8379074df~tplv-goo7wpa0wc-image.image)



</div>
</div>

## 2.7 以图搜图&以文搜图

<div type="doc-tabs">
<div type="tab-item" title="网页操作" key="chdkMCnaty">

成功完成以上步骤后，就可以使用API进行检索了，在页面上也可以进行快速检索测试。

1. 点击对应索引（best_practice_pic_search_index）右侧的”检索测试“。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/611b6e368d234b0a9d08a2bfc736bc57~tplv-goo7wpa0wc-image.image)

2. 输入文本，查询图片。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c92b2a0f07654d5a806cae7f41984ab5~tplv-goo7wpa0wc-image.image)

3. 也可以输入图片，查询图片。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6c76e2e3fbba4e2c82d89cb5660d0798~tplv-goo7wpa0wc-image.image)
注意，如果删除了TOS桶中的图片或者TOS桶本身，那么进行图片检索时则无法显示图片。

</div>
<div type="tab-item" title="Python操作" key="ZYTcS3nSZs">

成功完成以上步骤后，即可开始进行图片检索。以下示例展示了如何使用 Python 进行【以图搜图】和【以文搜图】，并将检索到的 Top10 图片下载到本地。

【以文搜图】操作说明：
 请在代码开头的 `Query` 位置填写您希望检索的文本内容。
 运行代码后，系统会自动将检索到的 Top10 图片下载到当前目录下的 `download_images` 文件夹中。
```Plain Text
# 文搜图
import json
import sys
import os
import requests # pip install requests
import tos # pip3 install --upgrade tos
from pprint import pprint
from volcengine.auth.SignerV4 import SignerV4 # pip3 install --upgrade volcengine
from volcengine.base.Request import Request # pip3 install --upgrade volcengine
from volcengine.Credentials import Credentials # pip3 install --upgrade volcengine

# 签名相关配置
AK = "*" # 输入您的AK，注意保留双引号
SK = "*" # 输入您的SK，注意保留双引号
DOMAIN = "api-vikingdb.volces.com"

# 检索参数配置
Collection_name = "best_practice_pic_search"
Index_name = "best_practice_pic_search_index"
Query ="熊猫"

# TOS 配置（请根据实际填写）
TOS_ENDPOINT = "tos-cn-beijing.volces.com"
TOS_REGION = "cn-beijing"
TOS_BUCKET = "best-practice-pic-search-tos"

# 本地保存路径
SAVE_DIR = "downloaded_images"
os.makedirs(SAVE_DIR, exist_ok=True)


# 签名请求生成函数
def prepare_request(method, path, ak, sk, params=None, data=None, doseq=0):
    if params:
        for key in params:
            if isinstance(params[key], (int, float, bool)):
                params[key] = str(params[key])
            elif sys.version_info[0] != 3 and isinstance(params[key], unicode):
                params[key] = params[key].encode("utf-8")
            elif isinstance(params[key], list) and not doseq:
                params[key] = ",".join(params[key])
    r = Request()
    r.set_shema("https")
    r.set_method(method)
    r.set_connection_timeout(10)
    r.set_socket_timeout(10)
    mheaders = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": DOMAIN,
    }
    r.set_headers(mheaders)
    if params:
        r.set_query(params)
    r.set_host(DOMAIN)
    r.set_path(path)
    if data is not None:
        r.set_body(json.dumps(data, ensure_ascii=False))
    credentials = Credentials(ak, sk, "air", "cn-north-1")
    SignerV4.sign(r, credentials)
    return r

# 检索请求参数
request_data = {
    "collection_name": "best_practice_pic_search",
    "index_name": "best_practice_pic_search_index",
    "search": {
        "order_by_raw": {
            "text": "熊猫"
        },
        "limit": 10
    }
}

# 发起检索请求
search_req = prepare_request(
    method="POST",
    path="/api/index/search",
    ak=AK,
    sk=SK,
    data=request_data
)

response = requests.request(
    method=search_req.method,
    url=f"https://{DOMAIN}{search_req.path}",
    headers=search_req.headers,
    data=search_req.body
)

# 解析结果
result = json.loads(response.text)
pprint(result)

# 下载图片函数
def download_tos_image(tos_uri, save_path):
    object_key = tos_uri.replace("tos://{}/".format(TOS_BUCKET), "")
    client = tos.TosClientV2(AK, SK, TOS_ENDPOINT, TOS_REGION)
    try:
        client.get_object_to_file(TOS_BUCKET, object_key, save_path)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {tos_uri}: {e}")

# 提取并下载图像
if result.get("code") == 0:
    data = result.get("data", [[]])[0]
    for item in data:
        tos_url = item.get("fields", {}).get("animal_image")
        if tos_url and tos_url.startswith("tos://"):
            filename = tos_url.split("/")[-1]
            local_path = os.path.join(SAVE_DIR, filename)
            download_tos_image(tos_url, local_path)
else:
    print("Search failed:", result.get("message"))
```

如下图所示，检索到的top10图片保存在了当前目录下的download_images文件夹中。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f06436bac8e74df7a2c2f87b0bb1f5e9~tplv-goo7wpa0wc-image.image)

【以图搜图】操作说明：
 请在代码开头的 `Query_Image_Path` 位置填写您希望用于检索的图片路径。
 运行代码后，系统会自动将检索到的 Top10 图片下载到当前目录下的 `download_images` 文件夹中。
```Plain Text
import json
import sys
import os
import base64
import requests        # pip install requests
import tos             # pip install volc-sdk-python
from pprint import pprint
from volcengine.auth.SignerV4 import SignerV4        # pip3 install --upgrade volcengine
from volcengine.base.Request import Request          # pip3 install --upgrade volcengine
from volcengine.Credentials import Credentials       # pip3 install --upgrade volcengine


# ===== 配置项 =====
AK = "*"  # 输入您的AK，注意保留双引号
SK = "*"  # 输入您的SK，注意保留双引号
Query_Image_Path = "*"  # 本地用于检索的图片路径
DOMAIN = "api-vikingdb.volces.com"  # VikingDB 的 API 域名

COLLECTION_NAME = "best_practice_pic_search"  # 检索的 Collection 名称
INDEX_NAME = "best_practice_pic_search_index"  # 检索的向量索引名称

TOS_ENDPOINT = "tos-cn-beijing.volces.com"  # TOS 的 endpoint（北京区域）
TOS_REGION = "cn-beijing"  # TOS 的 region（北京区域）
TOS_BUCKET = "best-practice-pic-search-tos"  # 存储图片的 TOS bucket 名称

SAVE_DIR = "downloaded_images"  # 检索结果图片下载保存的本地目录




os.makedirs(SAVE_DIR, exist_ok=True)


# ===== 读取本地图片并转为 Base64 =====
def encode_image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"base64://{encoded_string}"


# ===== 签名请求生成函数 =====
def prepare_request(method, path, ak, sk, params=None, data=None, doseq=0):
    if params:
        for key in params:
            if isinstance(params[key], (int, float, bool)):
                params[key] = str(params[key])
            elif sys.version_info[0] != 3 and isinstance(params[key], unicode):
                params[key] = params[key].encode("utf-8")
            elif isinstance(params[key], list) and not doseq:
                params[key] = ",".join(params[key])
    r = Request()
    r.set_shema("https")
    r.set_method(method)
    r.set_connection_timeout(10)
    r.set_socket_timeout(10)
    mheaders = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Host": DOMAIN,
    }
    r.set_headers(mheaders)
    if params:
        r.set_query(params)
    r.set_host(DOMAIN)
    r.set_path(path)
    if data is not None:
        r.set_body(json.dumps(data, ensure_ascii=False))
    credentials = Credentials(ak, sk, "air", "cn-north-1")
    SignerV4.sign(r, credentials)
    return r


# ===== 下载图片函数 =====
def download_tos_image(tos_uri, save_path):
    object_key = tos_uri.replace(f"tos://{TOS_BUCKET}/", "")
    client = tos.TosClientV2(AK, SK, TOS_ENDPOINT, TOS_REGION)
    try:
        client.get_object_to_file(TOS_BUCKET, object_key, save_path)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {tos_uri}: {e}")


# ===== 主函数：图搜图 + 下载 =====
def search_by_image(img_path):
    base64_img = encode_image_to_base64(img_path)

    request_data = {
        "collection_name": COLLECTION_NAME,
        "index_name": INDEX_NAME,
        "search": {
            "order_by_raw": {
                "image": base64_img
            },
            "limit": 10
        }
    }

    search_req = prepare_request(
        method="POST",
        path="/api/index/search",
        ak=AK,
        sk=SK,
        data=request_data
    )

    response = requests.request(
        method=search_req.method,
        url=f"https://{DOMAIN}{search_req.path}",
        headers=search_req.headers,
        data=search_req.body
    )

    result = json.loads(response.text)
    pprint(result)

    # 下载检索到的图片
    if result.get("code") == 0:
        data = result.get("data", [[]])[0]
        for item in data:
            tos_url = item.get("fields", {}).get("animal_image")
            if tos_url and tos_url.startswith("tos://"):
                filename = tos_url.split("/")[-1]
                local_path = os.path.join(SAVE_DIR, filename)
                download_tos_image(tos_url, local_path)
    else:
        print("Search failed:", result.get("message"))


# ===== 示例调用 =====
if __name__ == "__main__":
    image_path = Query_Image_Path
    search_by_image(image_path)
```

如下图所示，检索到的top10图片保存在了当前目录下的download_images文件夹中。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3e85c1bac17149efae4a31904eee67dc~tplv-goo7wpa0wc-image.image)
注意，如果删除了TOS桶中的图片或者TOS桶本身，那么进行图片检索时则无法保存结果图片到本地。

</div>
</div>


