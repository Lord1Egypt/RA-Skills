"""DXF 文档管理 - 创建、保存、版本、变量"""
import ezdxf
import os
from typing import Optional


# DXF 版本映射
DXF_VERSIONS = {
    'R2010':  'AC1024',
    'R2013':  'AC1027',
    'R2018':  'AC1032',
    'R2000':  'AC1015',
    'R2004':  'AC1018',
    'R2007':  'AC1021',
}


class CADDocument:
    """CAD 文档创建与管理"""

    @staticmethod
    def new(version: str = 'R2010',
           units: str = 'mm') -> ezdxf.document.Drawing:
        """
        创建新 DXF 文档
        
        Args:
            version: DXF 版本 ('R2010'/'R2013'/'R2018')
            units: 单位 ('mm'/'m'/'inch'/'ft')
        Returns:
            ezdxf Drawing 实例
        """
        ver_code = DXF_VERSIONS.get(version, 'AC1024')
        doc = ezdxf.new(ver_code)

        # 设置文档属性
        doc.header['$INSUNITS'] = _unit_code(units)
        
        # 设置默认文字样式
        try:
            style = doc.styles.get('STANDARD')
            style.dxf.height = 0  # 可变字高
            style.dxf.width_factor = 0.9
        except Exception:
            pass

        return doc

    @staticmethod
    def open(filepath: str) -> ezdxf.document.Drawing:
        """打开现有 DXF 文件"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        return ezdxf.readfile(filepath)

    @staticmethod
    def save(doc: ezdxf.document.Drawing, filepath: str, encoding: str = 'utf-8'):
        """
        保存 DXF 文件
        
        Args:
            encoding: 文件编码，中文内容用 utf-8
        """
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        doc.saveas(filepath, encoding=encoding)

    @staticmethod
    def msp(doc: ezdxf.document.Drawing):
        """获取模型空间"""
        return doc.modelspace()

    @staticmethod
    def set_metadata(doc,
                    title: str = '',
                    author: str = '',
                    subject: str = '',
                    comments: str = '',
                    keywords: str = ''):
        """设置文档元数据"""
        if hasattr(doc, 'header'):
            if title:
                try:
                    doc.header['$TITLE'] = title
                except Exception:
                    pass


def _unit_code(unit_name: str) -> int:
    """单位名称 → DXF INSUNITS 代码"""
    mapping = {
        'mm':      4,
        'm':       6,
        'cm':      5,
        'inch':    1,
        'ft':      2,
        'um':     13,   # 微米 (micrometer)
        'yd':      5,
        'mile':    10,
        'none':    0,   # 无单位
    }
    return mapping.get(unit_name.lower(), 0)
