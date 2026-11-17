from findskills import redundancy_groups


def test_redundant_pair_grouped():
    skills = [
        {"name": "A", "category": "x", "description": "PDF 读取 合并 拆分 转换 水印 处理"},
        {"name": "B", "category": "x", "description": "PDF 文件 读取 合并 拆分 转换 水印 工具"},
    ]
    groups = redundancy_groups(skills)
    assert len(groups) == 1
    assert set(groups[0]["members"]) == {"A", "B"}


def test_distinct_not_grouped():
    skills = [
        {"name": "A", "category": "x", "description": "PDF 读取 合并 拆分 水印 处理"},
        {"name": "B", "category": "y", "description": "股票 行情 基金 选股 财报 分析 交易"},
    ]
    assert redundancy_groups(skills) == []


def test_no_false_self_group():
    skills = [{"name": "A", "category": "x", "description": "PDF 处理"}]
    assert redundancy_groups(skills) == []
