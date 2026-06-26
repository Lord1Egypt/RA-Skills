#!/usr/bin/env python3
import sys, json

CONVERSIONS = {
    # 长度
    ('km','mi'): 0.621371, ('mi','km'): 1.60934,
    ('m','ft'): 3.28084, ('ft','m'): 0.3048,
    ('m','cm'): 100, ('cm','m'): 0.01,
    ('cm','inch'): 0.393701, ('inch','cm'): 2.54,
    ('km','m'): 1000, ('m','km'): 0.001,
    # 重量
    ('kg','lb'): 2.20462, ('lb','kg'): 0.453592,
    ('kg','g'): 1000, ('g','kg'): 0.001,
    ('g','oz'): 0.035274, ('oz','g'): 28.3495,
    ('kg','jin'): 2, ('jin','kg'): 0.5,
    # 温度
    ('c','f'): lambda c: c*9/5+32,
    ('f','c'): lambda f: (f-32)*5/9,
    ('c','k'): lambda c: c+273.15,
    ('k','c'): lambda k: k-273.15,
    # 容量
    ('l','ml'): 1000, ('ml','l'): 0.001,
    ('l','gal'): 0.264172, ('gal','l'): 3.78541,
    ('l','cup'): 4.22675, ('cup','l'): 0.236588,
    # 面积
    ('sqm','sqft'): 10.7639, ('sqft','sqm'): 0.092903,
    ('hectare','mu'): 15, ('mu','hectare'): 1/15,
    # 数据
    ('gb','mb'): 1024, ('mb','gb'): 1/1024,
    ('tb','gb'): 1024, ('gb','tb'): 1/1024,
    # 时间
    ('hour','min'): 60, ('min','hour'): 1/60,
    ('min','sec'): 60, ('sec','min'): 1/60,
    ('day','hour'): 24, ('hour','day'): 1/24,
}

def convert(value, from_unit, to_unit):
    key = (from_unit.lower(), to_unit.lower())
    if key in CONVERSIONS:
        rate = CONVERSIONS[key]
        if callable(rate):
            result = rate(value)
        else:
            result = value * rate
        return {'result': round(result, 4), 'from': f'{value}{from_unit}', 'to': f'{round(result, 4)}{to_unit}'}
    return {'error': '不支持的单位转换'}

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(json.dumps({'error': '用法: unit_converter.py <值> <单位1> <单位2>'}))
    else:
        print(json.dumps(convert(float(sys.argv[1]), sys.argv[2], sys.argv[3]), ensure_ascii=False))
