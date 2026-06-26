# 格式转换模块
import csv
import logging
from typing import Dict, List, Optional, Union
from pathlib import Path
from openpyxl import Workbook

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextConverter:
    """
    文本转换器类，支持非结构化文本转结构化 CSV/Excel
    """
    
    def __init__(self):
        """
        初始化文本转换器
        """
        pass
    
    def text_to_csv(self, text: str, output_file: Union[str, Path], 
                   delimiter: str = ',', headers: Optional[List[str]] = None) -> Dict[str, str]:
        """
        将文本转换为 CSV 文件
        
        Args:
            text: 要转换的文本
            output_file: 输出 CSV 文件路径
            delimiter: 分隔符，默认为 ','
            headers: 列标题列表，默认为 None
            
        Returns:
            转换结果状态
        """
        try:
            output_file = Path(output_file)
            
            # 简单的文本解析逻辑：按行分割，每行按空格分割为列
            lines = text.strip().split('\n')
            data = []
            
            for line in lines:
                if line.strip():
                    # 按空格分割，处理多个连续空格
                    columns = [col.strip() for col in line.split() if col.strip()]
                    data.append(columns)
            
            # 如果没有提供标题，使用默认标题
            if headers is None:
                max_columns = max(len(row) for row in data) if data else 0
                headers = [f'Column_{i+1}' for i in range(max_columns)]
            
            # 确保所有行的列数与标题一致
            for i in range(len(data)):
                while len(data[i]) < len(headers):
                    data[i].append('')
                data[i] = data[i][:len(headers)]
            
            # 写入 CSV 文件
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerow(headers)
                writer.writerows(data)
            
            return {
                "status": "success",
                "output_file": str(output_file),
                "rows_written": len(data)
            }
        except Exception as e:
            logger.error(f"转换为 CSV 时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def text_to_excel(self, text: str, output_file: Union[str, Path], 
                      sheet_name: str = 'Sheet1', headers: Optional[List[str]] = None) -> Dict[str, str]:
        """
        将文本转换为 Excel 文件
        
        Args:
            text: 要转换的文本
            output_file: 输出 Excel 文件路径
            sheet_name: 工作表名称，默认为 'Sheet1'
            headers: 列标题列表，默认为 None
            
        Returns:
            转换结果状态
        """
        try:
            output_file = Path(output_file)
            
            # 简单的文本解析逻辑：按行分割，每行按空格分割为列
            lines = text.strip().split('\n')
            data = []
            
            for line in lines:
                if line.strip():
                    # 按空格分割，处理多个连续空格
                    columns = [col.strip() for col in line.split() if col.strip()]
                    data.append(columns)
            
            # 如果没有提供标题，使用默认标题
            if headers is None:
                max_columns = max(len(row) for row in data) if data else 0
                headers = [f'Column_{i+1}' for i in range(max_columns)]
            
            # 确保所有行的列数与标题一致
            for i in range(len(data)):
                while len(data[i]) < len(headers):
                    data[i].append('')
                data[i] = data[i][:len(headers)]
            
            # 使用 openpyxl 直接创建 Excel 文件
            wb = Workbook()
            ws = wb.active
            ws.title = sheet_name
            
            # 写入标题
            if headers:
                ws.append(headers)
            
            # 写入数据
            for row in data:
                ws.append(row)
            
            # 保存文件
            wb.save(output_file)
            
            return {
                "status": "success",
                "output_file": str(output_file),
                "rows_written": len(data)
            }
        except Exception as e:
            logger.error(f"转换为 Excel 时出错: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def batch_convert(self, directory: Union[str, Path], output_format: str = 'csv',
                     **kwargs) -> List[Dict[str, str]]:
        """
        批量转换目录中的文本文件
        
        Args:
            directory: 目录路径
            output_format: 输出格式，可选 'csv' 或 'xlsx'
            **kwargs: 其他参数传递给转换函数
            
        Returns:
            转换结果列表
        """
        try:
            directory = Path(directory)
            if not directory.exists() or not directory.is_dir():
                return [{"error": "目录不存在或不是目录"}]
            
            results = []
            
            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == '.txt':
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()
                        
                        output_file = file_path.with_suffix(f'.{output_format}')
                        
                        if output_format == 'csv':
                            result = self.text_to_csv(text, output_file, **kwargs)
                        elif output_format == 'xlsx':
                            result = self.text_to_excel(text, output_file, **kwargs)
                        else:
                            result = {"status": "error", "error": "不支持的输出格式"}
                        
                        result["input_file"] = str(file_path)
                        results.append(result)
                    except Exception as e:
                        logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
                        results.append({
                            "input_file": str(file_path),
                            "status": "error",
                            "error": str(e)
                        })
            
            return results
        except Exception as e:
            logger.error(f"批量转换时出错: {str(e)}")
            return [{"error": str(e)}]
