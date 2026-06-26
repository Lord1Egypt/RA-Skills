import pandas as pd


def export(filePath, data) -> str:
    """
    将数据保存为excel文件
    :param filePath: 保存文件路径，如 E:\\Temp\\ReadingActivities\\text.xls
    :param data: 需要保存的数据，如 {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
    """
    if filePath.endswith(".xls"):
        return "不支持生成xls格式文件"

    df = pd.DataFrame(data)
    df.to_excel(filePath, index=False)
    return "保存成功"


if __name__ == '__main__':
    rel = export("E:\\Temp\\ReadingActivities\\text.xls", {'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
    print(rel)
