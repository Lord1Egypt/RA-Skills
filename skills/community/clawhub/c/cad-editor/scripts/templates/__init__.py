"""行业图库模块"""
from .architectural import ArchitecturalTemplates
from .mechanical import MechanicalTemplates
from .electrical import ElectricalTemplates
from .piping import PipingTemplates
from .structural import StructuralTemplates

__all__ = [
    'ArchitecturalTemplates', 'MechanicalTemplates', 
    'ElectricalTemplates', 'PipingTemplates', 'StructuralTemplates'
]
