#!/usr/bin/env python3
"""
Command registry for ChaoJi CLI.

Defines all supported commands, their parameters, and input aliases.
Based on 好麦算法 API documentation: https://doc.metac-inc.com/marketing/open-api.html
"""

# Command specifications
COMMAND_SPECS = {
    # ==================== 试衣试穿类 ====================
    
    'model_tryon_quick': {
        'requiredKeys': ['image_cloth', 'list_images_human'],
        'optionalKeys': ['cloth_length', 'dpi', 'output_format', 'batch_size', 'callBackUrl'],
        'arrayKeys': ['list_images_human'],
        'inputAliases': {
            'cloth': 'image_cloth',
            'cloth_image': 'image_cloth',
            'garment': 'image_cloth',
            'garment_image': 'image_cloth',
            '服装': 'image_cloth',
            '衣服': 'image_cloth',
            'model': 'list_images_human',
            'human': 'list_images_human',
            'person': 'list_images_human',
            '模特': 'list_images_human',
            '人物': 'list_images_human',
            'length': 'cloth_length',
            'cloth-length': 'cloth_length',
            '上身区域': 'cloth_length',
            'callback': 'callBackUrl',
            '回调 URL': 'callBackUrl',
        }
    },

    'human_tryon': {
        'requiredKeys': ['image_cloth', 'list_images_human', 'cloth_length'],
        'optionalKeys': ['dpi', 'output_format'],
        'arrayKeys': ['list_images_human'],
        'inputAliases': {
            'cloth': 'image_cloth',
            'cloth_image': 'image_cloth',
            'garment': 'image_cloth',
            'garment_image': 'image_cloth',
            '服装': 'image_cloth',
            '衣服': 'image_cloth',
            '服装图': 'image_cloth',
            'model': 'list_images_human',
            'human': 'list_images_human',
            'person': 'list_images_human',
            '模特': 'list_images_human',
            '人物': 'list_images_human',
            '模特图': 'list_images_human',
            'length': 'cloth_length',
            'cloth-length': 'cloth_length',
            '上身区域': 'cloth_length',
            '服装区域': 'cloth_length',
        }
    },
    
    'tryon_shoes': {
        'requiredKeys': ['list_images_shoe', 'list_images_human'],
        'optionalKeys': [],
        'arrayKeys': ['list_images_shoe', 'list_images_human'],
        'inputAliases': {
            'shoes': 'list_images_shoe',
            'shoe': 'list_images_shoe',
            'shoe_image': 'list_images_shoe',
            'image_shoe': 'list_images_shoe',
            '鞋': 'list_images_shoe',
            '鞋图': 'list_images_shoe',
            '鞋靴': 'list_images_shoe',
            '商品图': 'list_images_shoe',
            'model': 'list_images_human',
            'human': 'list_images_human',
            '模特': 'list_images_human',
            '模特图': 'list_images_human',
        }
    },
    
    # ==================== 图像生成类 ====================
    
    'image2image': {
        'requiredKeys': ['img', 'prompt'],
        'optionalKeys': ['ratio', 'resolution'],
        'arrayKeys': ['img'],
        'inputAliases': {
            'image': 'img',
            'images': 'img',
            '参考图': 'img',
            '图片': 'img',
            'reference': 'img',
            'text': 'prompt',
            '描述': 'prompt',
            '提示词': 'prompt',
            '比例': 'ratio',
            '分辨率': 'resolution',
        }
    },
    
    # ==================== 抠图类 ====================

    'cutout': {
        'requiredKeys': ['image'],
        'optionalKeys': ['method', 'cate_token'],
        'arrayKeys': [],
        'inputAliases': {
            '图片': 'image',
            '图像': 'image',
            '模式': 'method',
            'mode': 'method',
            '类别': 'cate_token',
            '服装类别': 'cate_token',
        }
    },

    # ==================== 查询类 ====================

    'remaining_quantity_of_beans': {
        'requiredKeys': [],
        'optionalKeys': [],
        'arrayKeys': [],
        'inputAliases': {}
    },
}

# Command aliases (short names)
COMMAND_ALIASES = {
    # 试衣试穿类 - 快速试衣
    'tryon-fast': 'model_tryon_quick',
    'tryon_fast': 'model_tryon_quick',
    'quick-tryon': 'model_tryon_quick',
    '快速试衣': 'model_tryon_quick',

    # 试衣试穿类 - 真人试衣（模特换装）
    'tryon': 'human_tryon',
    'human-tryon': 'human_tryon',
    '虚拟试衣': 'human_tryon',
    '试衣': 'human_tryon',
    '真人试衣': 'human_tryon',
    '模特换装': 'human_tryon',
    '换装': 'human_tryon',
    
    'tryon-shoes': 'tryon_shoes',
    'shoes-tryon': 'tryon_shoes',
    '试鞋': 'tryon_shoes',
    '鞋靴试穿': 'tryon_shoes',
    '鞋试穿': 'tryon_shoes',
    
    # 图像生成类
    'image-to-image': 'image2image',
    '图生图': 'image2image',
    '素材生成 - 图生图': 'image2image',
    'chao-paint': 'image2image',
    '潮绘': 'image2image',
    
    # 抠图类
    '抠图': 'cutout',
    '智能抠图': 'cutout',
    '通用抠图': 'cutout',
    '人像抠图': 'cutout',
    '服装分割': 'cutout',
    '图案抠图': 'cutout',
    'segmentation': 'cutout',
    'seg': 'cutout',

    # 查询类
    'beans': 'remaining_quantity_of_beans',
    '米豆': 'remaining_quantity_of_beans',
    '查询米豆': 'remaining_quantity_of_beans',
    '余额': 'remaining_quantity_of_beans',
    '剩余量': 'remaining_quantity_of_beans',
    'balance': 'remaining_quantity_of_beans',
}

# Video commands (require longer timeout)
VIDEO_COMMANDS = []

# Model type mappings for better user experience
MODEL_TYPE_MAPPINGS = {
    'image2image': {
        'chao_paint_3.0pro': 'chao_paint_3.0pro',
        'chao_paint_3.0': 'chao_paint_3.0',
        'chao_paint_2.0pro': 'chao_paint_2.0pro',
        'chao_paint_2.0': 'chao_paint_2.0',
        'chao_paint_1.0': 'chao_paint_1.0',
        '3.0pro': 'chao_paint_3.0pro',
        '3.0': 'chao_paint_3.0',
        '2.0pro': 'chao_paint_2.0pro',
        '2.0': 'chao_paint_2.0',
        '1.0': 'chao_paint_1.0',
    },
}


def normalize_lookup_key(value):
    """Normalize a key for lookup (case-insensitive, strip whitespace)."""
    return str(value or '').strip().lower()


def build_command_alias_lookup():
    """Build a lookup dictionary for command aliases."""
    lookup = {}
    
    # Add command names themselves
    for command_name in COMMAND_SPECS.keys():
        key = normalize_lookup_key(command_name)
        if key:
            lookup[key] = command_name
        # Also add underscore to hyphen conversion
        underscore = normalize_lookup_key(command_name.replace('-', '_'))
        if underscore:
            lookup[underscore] = command_name
    
    # Add aliases
    for alias, target in COMMAND_ALIASES.items():
        key = normalize_lookup_key(alias)
        if key:
            lookup[key] = target
    
    return lookup


COMMAND_ALIAS_LOOKUP = build_command_alias_lookup()


def resolve_command_alias(command):
    """
    Resolve a command alias to its canonical name.
    
    Args:
        command: Command name or alias
        
    Returns:
        Canonical command name
        
    Raises:
        ValueError: If command is not supported
    """
    key = normalize_lookup_key(command)
    resolved = COMMAND_ALIAS_LOOKUP.get(key)
    
    if not resolved or resolved not in COMMAND_SPECS:
        raise ValueError(f"unsupported command: {command}")
    
    return resolved


def get_command_spec(command):
    """
    Get the specification for a command.
    
    Args:
        command: Command name (must be canonical)
        
    Returns:
        Command specification dictionary
    """
    return COMMAND_SPECS.get(command, {})


def normalize_input_keys(command, input_data):
    """
    Normalize input keys using aliases.
    
    Args:
        command: Command name (must be canonical)
        input_data: Input dictionary with possible alias keys
        
    Returns:
        Normalized input dictionary with canonical keys
    """
    spec = COMMAND_SPECS.get(command, {})
    input_aliases = spec.get('inputAliases', {})
    
    # Build reverse lookup (alias -> canonical)
    alias_to_canonical = {}
    for alias, canonical in input_aliases.items():
        alias_to_canonical[normalize_lookup_key(alias)] = canonical
    
    # Normalize keys
    normalized = {}
    for key, value in input_data.items():
        normalized_key = normalize_lookup_key(key)
        canonical_key = alias_to_canonical.get(normalized_key, key)
        normalized[canonical_key] = value
    
    return normalized


def get_model_type_value(command, model_type_str):
    """
    Get the actual model type value from user-friendly string.
    
    Args:
        command: Command name
        model_type_str: User-friendly model type string
        
    Returns:
        Actual model type value for API
    """
    mappings = MODEL_TYPE_MAPPINGS.get(command, {})
    normalized = normalize_lookup_key(model_type_str)
    return mappings.get(normalized, model_type_str)
