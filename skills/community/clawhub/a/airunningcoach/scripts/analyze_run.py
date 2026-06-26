#!/usr/bin/env python3
"""
跑步数据分析脚本
解析 TCX/GPX 文件，分析配速、心率、步频等数据
"""

import argparse
import json
import xml.etree.ElementTree as ET
import sys
from datetime import datetime

def parse_gpx(file_path):
    """解析 GPX 文件"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 处理 GPX 命名空间
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        
        tracks = []
        for trk in root.findall('.//gpx:trk', ns):
            track_data = {
                'name': trk.findtext('gpx:name', '', ns),
                'points': []
            }
            
            for trkseg in trk.findall('.//gpx:trkseg', ns):
                for trkpt in trkseg.findall('gpx:trkpt', ns):
                    point = {
                        'lat': float(trkpt.get('lat')),
                        'lon': float(trkpt.get('lon')),
                        'time': trkpt.findtext('gpx:time', '', ns)
                    }
                    
                    # 扩展数据
                    extensions = trkpt.find('gpx:extensions', ns)
                    if extensions is not None:
                        for child in extensions:
                            tag = child.tag.split('}')[-1]  # 移除命名空间
                            if child.text:
                                try:
                                    point[tag] = float(child.text)
                                except ValueError:
                                    point[tag] = child.text
                    
                    track_data['points'].append(point)
            
            tracks.append(track_data)
        
        return tracks
    except Exception as e:
        print(f"解析 GPX 失败：{e}", file=sys.stderr)
        return None

def parse_tcx(file_path):
    """解析 TCX 文件"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # TCX 命名空间
        ns = {
            'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        
        activities = []
        for activity in root.findall('.//tcx:Activity', ns):
            act_type = activity.get('Sport', 'Running')
            act_data = {
                'sport': act_type,
                'laps': [],
                'total_distance': 0,
                'total_time': 0
            }
            
            for lap in activity.findall('.//tcx:Lap', ns):
                lap_data = {
                    'distance': float(lap.findtext('tcx:DistanceMeters', '0', ns)),
                    'time': lap.findtext('tcx:TotalTimeSeconds', '0', ns),
                    'calories': int(lap.findtext('tcx:Calories', '0', ns)),
                    'avg_hr': None,
                    'max_hr': None,
                    'points': []
                }
                
                # 心率数据
                tpx = lap.find('.//tcx:TPX', {'tpx': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'})
                if tpx is not None:
                    lap_data['avg_hr'] = tpx.findtext('{http://www.garmin.com/xmlschemas/ActivityExtension/v2}AverageHeartRateBpm')
                    lap_data['max_hr'] = tpx.findtext('{http://www.garmin.com/xmlschemas/ActivityExtension/v2}MaximumHeartRateBpm')
                
                # 轨迹点
                for track in lap.findall('.//tcx:Track', ns):
                    for tp in track.findall('tcx:Trackpoint', ns):
                        point = {
                            'time': tp.findtext('tcx:Time', '', ns),
                            'distance': float(tp.findtext('tcx:DistanceMeters', '0', ns)) if tp.findtext('tcx:DistanceMeters') else None,
                        }
                        
                        # 心率
                        hr_elem = tp.find('tcx:HeartRateBpm/tcx:Value', ns)
                        if hr_elem is not None:
                            point['hr'] = int(hr_elem.text)
                        
                        # 步频
                        tpx = tp.find('tcx:TPX', {'tpx': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'})
                        if tpx is not None:
                            cadence = tpx.findtext('{http://www.garmin.com/xmlschemas/ActivityExtension/v2}RunCadence')
                            if cadence:
                                point['cadence'] = int(cadence)
                        
                        lap_data['points'].append(point)
                
                act_data['laps'].append(lap_data)
                act_data['total_distance'] += lap_data['distance']
                act_data['total_time'] += float(lap_data['time'])
            
            activities.append(act_data)
        
        return activities
    except Exception as e:
        print(f"解析 TCX 失败：{e}", file=sys.stderr)
        return None

def analyze_activity(data):
    """分析活动数据"""
    if not data:
        return None
    
    analysis = {
        'total_distance_km': 0,
        'total_time_sec': 0,
        'avg_pace': None,
        'avg_hr': None,
        'max_hr': None,
        'avg_cadence': None,
        'hr_zones': {},
        'elevation_gain': 0
    }
    
    # 处理 TCX 格式
    if isinstance(data, list) and len(data) > 0:
        for activity in data:
            analysis['total_distance_km'] += activity.get('total_distance', 0) / 1000
            analysis['total_time_sec'] += activity.get('total_time', 0)
            
            all_hr = []
            all_cadence = []
            
            for lap in activity.get('laps', []):
                if lap.get('avg_hr'):
                    all_hr.append(int(lap['avg_hr']))
                if lap.get('max_hr'):
                    if analysis['max_hr'] is None or int(lap['max_hr']) > analysis['max_hr']:
                        analysis['max_hr'] = int(lap['max_hr'])
                
                for point in lap.get('points', []):
                    if 'hr' in point:
                        all_hr.append(point['hr'])
                    if 'cadence' in point:
                        all_cadence.append(point['cadence'])
            
            if all_hr:
                analysis['avg_hr'] = round(sum(all_hr) / len(all_hr))
            if all_cadence:
                analysis['avg_cadence'] = round(sum(all_cadence) / len(all_cadence))
    
    # 计算平均配速
    if analysis['total_distance_km'] > 0 and analysis['total_time_sec'] > 0:
        pace_sec_per_km = analysis['total_time_sec'] / analysis['total_distance_km']
        mins = int(pace_sec_per_km // 60)
        secs = int(pace_sec_per_km % 60)
        analysis['avg_pace'] = f"{mins}:{secs:02d}"
    
    return analysis

def main():
    parser = argparse.ArgumentParser(description="跑步数据分析")
    parser.add_argument("file", help="TCX 或 GPX 文件路径")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 解析文件
    if args.file.endswith('.gpx'):
        data = parse_gpx(args.file)
    elif args.file.endswith('.tcx'):
        data = parse_tcx(args.file)
    else:
        print("不支持的文件格式，请使用 .gpx 或 .tcx", file=sys.stderr)
        sys.exit(1)
    
    if not data:
        print("文件解析失败", file=sys.stderr)
        sys.exit(1)
    
    # 分析数据
    analysis = analyze_activity(data)
    
    if args.output == "json":
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*50}")
        print("跑步数据分析")
        print(f"{'='*50}")
        print(f"总距离：{analysis['total_distance_km']:.2f} km")
        print(f"总时间：{analysis['total_time_sec']/3600:.2f} 小时")
        print(f"平均配速：{analysis['avg_pace']} /km")
        if analysis['avg_hr']:
            print(f"平均心率：{analysis['avg_hr']} bpm")
        if analysis['max_hr']:
            print(f"最大心率：{analysis['max_hr']} bpm")
        if analysis['avg_cadence']:
            print(f"平均步频：{analysis['avg_cadence']} spm")
        print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
