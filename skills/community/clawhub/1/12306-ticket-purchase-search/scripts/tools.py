from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_current_date(
) -> Dict[str, Any]:
    """
    获取当前日期，以上海时区（Asia/Shanghai, UTC+8）为准，返回格式为 "yyyy-MM-dd"。主要用于解析用户提到的相对日期（如“明天”、“下周三”），提供准确的日期输入。
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659202051", "get_current_date", arguments)

def get_stations_code_in_city(
    city: str
) -> Dict[str, Any]:
    """
    通过中文城市名查询该城市 **所有** 火车站的名称及其对应的 `station_code`，结果是一个包含多个车站信息的列表。
    
    Args:
        city: 中文城市名称，例如："北京", "上海"
    
    Returns:
        
    """
    arguments = {
        "city": city
    }
    
    return call_api("1777316659202051", "get_stations_code_in_city", arguments)

def get_station_code_of_citys(
    citys: str
) -> Dict[str, Any]:
    """
    通过中文城市名查询代表该城市的 `station_code`。此接口主要用于在用户提供**城市名**作为出发地或到达地时，为接口准备 `station_code` 参数。
    
    Args:
        citys: 要查询的城市，比如"北京"。若要查询多个城市，请用|分割，比如"北京|上海"。
    
    Returns:
        
    """
    arguments = {
        "citys": citys
    }
    
    return call_api("1777316659202051", "get_station_code_of_citys", arguments)

def get_station_code_by_names(
    stationNames: str
) -> Dict[str, Any]:
    """
    通过具体的中文车站名查询其 `station_code` 和车站名。此接口主要用于在用户提供**具体车站名**作为出发地或到达地时，为接口准备 `station_code` 参数。
    
    Args:
        stationNames: 具体的中文车站名称，例如："北京南", "上海虹桥"。若要查询多个站点，请用|分割，比如"北京南|上海虹桥"。
    
    Returns:
        
    """
    arguments = {
        "stationNames": stationNames
    }
    
    return call_api("1777316659202051", "get_station_code_by_names", arguments)

def get_station_by_telecode(
    stationTelecode: str
) -> Dict[str, Any]:
    """
    通过车站的 `station_telecode` 查询车站的详细信息，包括名称、拼音、所属城市等。此接口主要用于在已知 `telecode` 的情况下获取更完整的车站数据，或用于特殊查询及调试目的。一般用户对话流程中较少直接触发。
    
    Args:
        stationTelecode: 车站的 `station_telecode` (3位字母编码)
    
    Returns:
        
    """
    arguments = {
        "stationTelecode": stationTelecode
    }
    
    return call_api("1777316659202051", "get_station_by_telecode", arguments)

def get_tickets(
    date: str,
    fromStation: str,
    toStation: str,
    trainFilterFlags: Optional[str] = "",
    earliestStartTime: Optional[float] = 0.0,
    latestStartTime: Optional[float] = 24.0,
    sortFlag: Optional[str] = "",
    sortReverse: Optional[bool] = False,
    limitedNum: Optional[float] = 0.0,
    format: Optional[str] = "text"
) -> Dict[str, Any]:
    """
    查询12306余票信息。
    
    Args:
        date: 查询日期，格式为 "yyyy-MM-dd"。如果用户提供的是相对日期（如“明天”），请务必先调用 `get-current-date` 接口获取当前日期，并计算出目标日期。
        fromStation: 出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。
        toStation: 到达地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。
        trainFilterFlags: 车次筛选条件，默认为空，即不筛选。支持多个标志同时筛选。例如用户说“高铁票”，则应使用 "G"。可选标志：[G(高铁/城际),D(动车),Z(直达特快),T(特快),K(快速),O(其他),F(复兴号),S(智能动车组)]
        earliestStartTime: 最早出发时间（0-24），默认为0。
        latestStartTime: 最迟出发时间（0-24），默认为24。
        sortFlag: 排序方式，默认为空，即不排序。仅支持单一标识。可选标志：[startTime(出发时间从早到晚), arriveTime(抵达时间从早到晚), duration(历时从短到长)]
        sortReverse: 是否逆向排序结果，默认为false。仅在设置了sortFlag时生效。
        limitedNum: 返回的余票数量限制，默认为0，即不限制。
        format: 返回结果格式，默认为text，建议使用text与csv。可选标志：[text, csv, json]
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "fromStation": fromStation,
        "toStation": toStation,
        "trainFilterFlags": trainFilterFlags,
        "earliestStartTime": earliestStartTime,
        "latestStartTime": latestStartTime,
        "sortFlag": sortFlag,
        "sortReverse": sortReverse,
        "limitedNum": limitedNum,
        "format": format
    }
    
    return call_api("1777316659202051", "get_tickets", arguments)

def get_interline_tickets(
    date: str,
    fromStation: str,
    toStation: str,
    middleStation: Optional[str] = "",
    showWZ: Optional[bool] = False,
    trainFilterFlags: Optional[str] = "",
    earliestStartTime: Optional[float] = 0.0,
    latestStartTime: Optional[float] = 24.0,
    sortFlag: Optional[str] = "",
    sortReverse: Optional[bool] = False,
    limitedNum: Optional[float] = 10.0,
    format: Optional[str] = "text"
) -> Dict[str, Any]:
    """
    查询12306中转余票信息。尚且只支持查询前十条。
    
    Args:
        date: 查询日期，格式为 "yyyy-MM-dd"。如果用户提供的是相对日期（如“明天”），请务必先调用 `get-current-date` 接口获取当前日期，并计算出目标日期。
        fromStation: 出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。
        toStation: 出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。
        middleStation: 中转地的 `station_code` ，可选。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。
        showWZ: 是否显示无座车，默认不显示无座车。
        trainFilterFlags: 车次筛选条件，默认为空。从以下标志中选取多个条件组合[G(高铁/城际),D(动车),Z(直达特快),T(特快),K(快速),O(其他),F(复兴号),S(智能动车组)]
        earliestStartTime: 最早出发时间（0-24），默认为0。
        latestStartTime: 最迟出发时间（0-24），默认为24。
        sortFlag: 排序方式，默认为空，即不排序。仅支持单一标识。可选标志：[startTime(出发时间从早到晚), arriveTime(抵达时间从早到晚), duration(历时从短到长)]
        sortReverse: 是否逆向排序结果，默认为false。仅在设置了sortFlag时生效。
        limitedNum: 返回的中转余票数量限制，默认为10。
        format: 返回结果格式，默认为text，建议使用text。可选标志：[text, json]
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "fromStation": fromStation,
        "toStation": toStation,
        "middleStation": middleStation,
        "showWZ": showWZ,
        "trainFilterFlags": trainFilterFlags,
        "earliestStartTime": earliestStartTime,
        "latestStartTime": latestStartTime,
        "sortFlag": sortFlag,
        "sortReverse": sortReverse,
        "limitedNum": limitedNum,
        "format": format
    }
    
    return call_api("1777316659202051", "get_interline_tickets", arguments)

def get_train_route_stations(
    trainCode: str,
    departDate: str,
    format: Optional[str] = "text"
) -> Dict[str, Any]:
    """
    查询特定列车车次在指定区间内的途径车站、到站时间、出发时间及停留时间等详细经停信息。当用户询问某趟具体列车的经停站时使用此接口。
    
    Args:
        trainCode: 要查询的车次 `train_code`，例如"G1033"。
        departDate: 列车出发的日期 (格式: yyyy-MM-dd)。如果用户提供的是相对日期，请务必先调用 `get-current-date` 解析。
        format: 返回结果格式，默认为text，建议使用text。可选标志：[text, json]
    
    Returns:
        
    """
    arguments = {
        "trainCode": trainCode,
        "departDate": departDate,
        "format": format
    }
    
    return call_api("1777316659202051", "get_train_route_stations", arguments)

