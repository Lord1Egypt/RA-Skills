#!/usr/bin/env python3
"""
Genos DNA 序列分析脚本
用于通用 Skill 系统调用 Genos 模型进行 DNA 分析
"""

import sys
import json
import re
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 模型路径配置
# 可以通过环境变量 GENOS_MODEL_PATH 自定义模型路径
# 默认路径为 ./models/Genos-1___2B (相对于项目根目录)
_model_path_env = os.environ.get('GENOS_MODEL_PATH', './models/Genos-1___2B')

# 模型状态文件路径
# 可以通过环境变量 GENOS_STATUS_FILE 自定义状态文件路径
# 默认路径为 scripts/.model_loaded (相对于项目根目录)
# 使用 scripts/ 目录而不是根目录，避免影响 ClawHub 发布
_model_status_file_env = os.environ.get('GENOS_STATUS_FILE', './scripts/.model_loaded')

# 加载配置文件（如果存在）
_config = None
def load_config():
    """从 config.json 加载配置"""
    global _config
    if _config is None:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    _config = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config.json: {e}", file=sys.stderr)
                _config = {}
        else:
            _config = {}
    return _config

# 使用环境变量作为默认值
model_path = _model_path_env
model_status_file = _model_status_file_env

# 如果有配置文件，仅在环境变量未设置时使用配置文件中的值
config = load_config()
if 'model_path' in config and not os.environ.get('GENOS_MODEL_PATH'):
    model_path = config['model_path']
if 'state_file' in config and not os.environ.get('GENOS_STATUS_FILE'):
    model_status_file = config['state_file']

_model = None
_tokenizer = None


def is_model_loaded():
    """检查模型是否已加载"""
    if os.path.exists(model_status_file):
        with open(model_status_file, 'r') as f:
            return f.read().strip() == 'loaded'
    return False


def set_model_loaded():
    """标记模型已加载"""
    # 确保目录存在
    model_status_dir = os.path.dirname(model_status_file)
    if model_status_dir and not os.path.exists(model_status_dir):
        os.makedirs(model_status_dir, exist_ok=True)
    with open(model_status_file, 'w') as f:
        f.write('loaded')


def load_model():
    """加载 Genos 模型"""
    global _model, _tokenizer
    if _model is None:
        print("Loading Genos model...", file=sys.stderr)
        _tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
        _model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="cpu",
            trust_remote_code=True,
            local_files_only=True
        )
        print("Model loaded successfully!", file=sys.stderr)
        set_model_loaded()
    return _model, _tokenizer


def clean_dna_sequence(sequence):
    """清理 DNA 序列，只保留有效碱基"""
    sequence = sequence.upper()
    sequence = re.sub(r'[^ACGTN]', '', sequence)
    return sequence


def analyze_dna_sequence(sequence):
    """
    分析 DNA 序列
    输入: DNA 序列字符串
    返回: 分析结果字典
    """
    model, tokenizer = load_model()

    original_seq = sequence
    sequence = clean_dna_sequence(sequence)

    if not sequence:
        return {"error": "无效的 DNA 序列，请只包含 A, C, G, T, N 碱基字符"}

    base_count = len(sequence)
    base_freq = {
        'A': sequence.count('A'),
        'C': sequence.count('C'),
        'G': sequence.count('G'),
        'T': sequence.count('T'),
        'N': sequence.count('N')
    }

    result = {
        "original_length": len(original_seq),
        "cleaned_length": base_count,
        "gc_content": round((base_freq['G'] + base_freq['C']) / base_count * 100, 2) if base_count > 0 else 0,
        "base_composition": {
            "A": round(base_freq['A'] / base_count * 100, 2) if base_count > 0 else 0,
            "C": round(base_freq['C'] / base_count * 100, 2) if base_count > 0 else 0,
            "G": round(base_freq['G'] / base_count * 100, 2) if base_count > 0 else 0,
            "T": round(base_freq['T'] / base_count * 100, 2) if base_count > 0 else 0,
            "N": round(base_freq['N'] / base_count * 100, 2) if base_count > 0 else 0
        }
    }

    return result


def predict_next_base(sequence, top_k=3):
    """
    预测 DNA 序列的下一个碱基
    输入: DNA 序列
    返回: 预测结果
    """
    model, tokenizer = load_model()

    sequence = clean_dna_sequence(sequence)

    if not sequence:
        return {"error": "无效的 DNA 序列"}

    if len(sequence) < 1:
        return {"error": "序列太短，无法预测"}

    if tokenizer is None:
        return {"error": "Tokenizer 未初始化"}
    
    inputs = tokenizer(sequence, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[0, -1]
        probs = torch.softmax(logits, dim=-1)

    top_indices = torch.topk(probs, min(top_k, len(probs)))

    base_names = {5: 'C', 6: 'G', 7: 'T', 8: 'A', 9: 'N', 0: '[PAD]', 1: '[UNK]', 2: '[CLS]', 3: '[SEP]', 4: '[MASK]'}
    predictions = []
    for idx, prob in zip(top_indices.indices, top_indices.values):
        idx_int = int(idx.item())
        base = base_names.get(idx_int, f"token_{idx_int}")
        predictions.append({
            "base": base,
            "probability": round(prob.item(), 4)
        })

    return {
        "input_sequence": sequence[-10:] + "..." if len(sequence) > 10 else sequence,
        "predictions": predictions
    }


def extract_sequence_features(sequence):
    """
    提取 DNA 序列特征
    输入: DNA 序列
    返回: 特征字典
    """
    model, tokenizer = load_model()

    sequence = clean_dna_sequence(sequence)

    if not sequence:
        return {"error": "无效的 DNA 序列"}

    base_count = len(sequence)
    base_freq = {
        'A': sequence.count('A'),
        'C': sequence.count('C'),
        'G': sequence.count('G'),
        'T': sequence.count('T'),
        'N': sequence.count('N')
    }

    gc = (base_freq['G'] + base_freq['C']) / base_count * 100 if base_count > 0 else 0
    at = (base_freq['A'] + base_freq['T']) / base_count * 100 if base_count > 0 else 0

    features = {
        "length": base_count,
        "base_composition": {
            "A": f"{base_freq['A']/base_count*100:.2f}%",
            "C": f"{base_freq['C']/base_count*100:.2f}%",
            "G": f"{base_freq['G']/base_count*100:.2f}%",
            "T": f"{base_freq['T']/base_count*100:.2f}%",
            "N": f"{base_freq['N']/base_count*100:.2f}%"
        },
        "gc_content": f"{gc:.2f}%",
        "at_content": f"{at:.2f}%",
        "model_info": {
            "name": "Genos-1.2B",
            "type": "Genomics Foundation Model",
            "parameters": "1.2B",
            "organization": "Zhejiang Lab"
        }
    }

    return features


def main():
    """CLI 入口点"""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python script.py <function> <sequence>"}))
        sys.exit(1)

    function_name = sys.argv[1]
    sequence = sys.argv[2]

    if function_name == "analyze":
        result = analyze_dna_sequence(sequence)
    elif function_name == "predict":
        result = predict_next_base(sequence)
    elif function_name == "features":
        result = extract_sequence_features(sequence)
    else:
        result = {"error": f"未知函数: {function_name}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
