"""图层管理器 - 创建/配置图层"""
import ezdxf
from typing import Optional


# 行业标准图层配置模板
LAYER_TEMPLATES = {
    # 建筑制图 (GB/T 50001)
    'arch': [
        {'name': 'wall',        'color': 1,   'linetype': 'Continuous', 'desc': '墙体'},
        {'name': 'door',        'color': 3,   'linetype': 'Continuous', 'desc': '门'},
        {'name': 'window',      'color': 4,   'linetype': 'Continuous', 'desc': '窗'},
        {'name': 'furniture',   'color': 5,   'linetype': 'Continuous', 'desc': '家具'},
        {'name': 'dimension',   'color': 2,   'linetype': 'Continuous', 'desc': '尺寸标注'},
        {'name': 'text',        'color': 7,   'linetype': 'Continuous', 'desc': '文字注释'},
        {'name': 'hatch',       'color': 8,   'linetype': 'Continuous', 'desc': '填充图案'},
        {'name': 'axis',        'color': 1,   'linetype': 'CENTER',    'desc': '轴线'},
        {'name': 'column',      'color': 2,   'linetype': 'Continuous', 'desc': '柱子'},
        {'name': 'stair',       'color': 4,   'linetype': 'Continuous', 'desc': '楼梯'},
        {'name': 'balcony',     'color': 5,   'linetype': 'Continuous', 'desc': '阳台'},
    ],
    # 机械制图 (GB/T 4457)
    'mech': [
        {'name': 'outline',     'color': 7,   'linetype': 'Continuous', 'desc': '轮廓线（粗实线）'},
        {'name': 'hidden',      'color': 2,   'linetype': 'DASHED',    'desc': '隐藏线'},
        {'name': 'center',      'color': 1,   'linetype': 'CENTER2',   'desc': '中心线'},
        {'name': 'dimension',   'color': 3,   'linetype': 'Continuous', 'desc': '尺寸线'},
        {'name': 'hatch',       'color': 8,   'linetype': 'Continuous', 'desc': '剖面线'},
        {'name': 'text',        'color': 7,   'linetype': 'Continuous', 'desc': '技术要求'},
        {'name': 'thin',        'color': 5,   'linetype': 'Continuous', 'desc': '细实线'},
        {'name': 'phantom',     'color': 6,   'linetype': 'PHANTOM2',  'desc': '假想线'},
    ],
    # 电气制图
    'elec': [
        {'name': 'wire',        'color': 7,   'linetype': 'Continuous', 'desc': '导线'},
        {'name': 'device',      'color': 3,   'linetype': 'Continuous', 'desc': '设备轮廓'},
        {'name': 'symbol',      'color': 1,   'linetype': 'Continuous', 'desc': '电气符号'},
        {'name': 'annotation',  'color': 4,   'linetype': 'Continuous', 'desc': '标注说明'},
        {'name': 'grid',        'color': 8,   'linetype': 'DOTTED',    'desc': '网格'},
    ],
    # 管道/暖通
    'piping': [
        {'name': 'pipe',        'color': 2,   'linetype': 'Continuous', 'desc': '管道'},
        {'name': 'valve',       'color': 3,   'linetype': 'Continuous', 'desc': '阀门'},
        {'name': 'fitting',     'color': 5,   'linetype': 'Continuous', 'desc': '管件'},
        {'name': 'insulation',  'color': 8,   'linetype': 'DASHDOT',    'desc': '保温层'},
        {'name': 'dimension',   'color': 7,   'linetype': 'Continuous', 'desc': '标注'},
    ],
    # 结构详图 (GB/T 50105)
    'struct': [
        {'name': 'outline',     'color': 7,   'linetype': 'Continuous', 'desc': '轮廓线（粗实线）'},
        {'name': 'rebar',       'color': 1,   'linetype': 'Continuous', 'desc': '钢筋线'},
        {'name': 'hatch',       'color': 8,   'linetype': 'Continuous', 'desc': '混凝土填充'},
        {'name': 'column',      'color': 2,   'linetype': 'Continuous', 'desc': '柱截面'},
        {'name': 'axis',        'color': 1,   'linetype': 'CENTER',     'desc': '轴线'},
        {'name': 'text',        'color': 7,   'linetype': 'Continuous', 'desc': '标注文字'},
        {'name': 'dimension',   'color': 3,   'linetype': 'Continuous', 'desc': '尺寸标注'},
        {'name': 'thin',        'color': 5,   'linetype': 'Continuous', 'desc': '细实线/分布筋'},
    ],
}


class LayerManager:
    """图层管理"""

    def __init__(self, doc: ezdxf.document.Drawing):
        self.doc = doc

    def create(self, 
               name: str,
               color: int = 7,
               linetype: str = 'Continuous',
               lineweight: int = -1,
               frozen: bool = False,
               locked: bool = False,
               plot: bool = True):
        """
        创建或获取图层
        
        Args:
            color: ACI 颜色索引 (1=红, 2=黄, 3=绿, 4=青, 5=蓝, 6=品红, 7=白)
            lineweight: 线重 (1/100 mm)，如 50=0.5mm，-1=默认
            frozen: 是否冻结
            locked: 是否锁定
            plot: 是否打印
        """
        try:
            layer = self.doc.layers.new(name)
        except ezdxf.DXFTableEntryError:
            layer = self.doc.layers.get(name)

        layer.color = color
        
        # 设置线型（如果存在）
        if linetype != 'Continuous':
            try:
                self.doc.linetypes.get(linetype)
                layer.dxf.linetype = linetype
            except Exception:
                pass  # 线型不存在则忽略
                
        if lineweight > 0:
            layer.dxf.lineweight = lineweight
            
        if frozen:
            layer.freeze()
        if locked:
            layer.lock()
        if not plot:
            layer.plot(False)
            
        return layer

    def setup_template(self, template_name: str) -> list:
        """应用行业标准图层模板"""
        if template_name not in LAYER_TEMPLATES:
            raise ValueError(f"未知模板: {template_name}，可用: {list(LAYER_TEMPLATES.keys())}")
        
        layers = []
        valid_keys = {'name','color','linetype','lineweight','frozen','locked','plot'}
        for cfg in LAYER_TEMPLATES[template_name]:
            filtered = {k:v for k,v in cfg.items() if k in valid_keys}
            layer = self.create(**filtered)
            layers.append(layer)
        return layers

    def list_layers(self) -> list:
        """列出所有图层信息"""
        result = []
        for layer in self.doc.layers:
            result.append({
                'name': layer.dxf.name,
                'color': layer.dxf.color,
                'linetype': layer.dxf.linetype,
                'is_frozen': layer.is_frozen(),
                'is_locked': layer.is_locked(),
            })
        return result

    def set_current(self, name: str):
        """设置当前图层"""
        try:
            self.doc.layers.set(name)
        except Exception:
            pass

    def freeze(self, name: str):
        self.doc.layers.get(name).freeze()

    def unfreeze(self, name: str):
        self.doc.layers.get(name).unfreeze()

    def lock(self, name: str):
        self.doc.layers.get(name).lock()

    def unlock(self, name: str):
        self.doc.layers.get(name).unlock()
