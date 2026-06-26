
import time
import argparse
import json
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def query_chaoyang_school(community_name):
    """朝阳区：通过浏览器自动化查询 xqcx.bjchyedu.cn"""
    print(f"[{community_name}] 正在启动浏览器自动查询朝阳区学区信息...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    result_data = {
        "district": "朝阳",
        "community": community_name,
        "schools": [],
        "status": "success",
        "message": ""
    }

    try:
        driver.get("http://xqcx.bjchyedu.cn/")
        wait = WebDriverWait(driver, 15)
        
        # 1. Input community name
        input_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
        driver.execute_script("arguments[0].value = '';", input_field)
        time.sleep(0.5)
        
        for char in community_name:
            input_field.send_keys(char)
            time.sleep(0.1)
            
        time.sleep(1.5)
        
        # Try to click autocomplete suggestion
        try:
            autocomplete_list = driver.find_elements(By.CLASS_NAME, "autocomplete-suggestion")
            if autocomplete_list:
                for item in autocomplete_list:
                    if community_name in item.text:
                        item.click()
                        time.sleep(0.5)
                        break
                else:
                    autocomplete_list[0].click()
                    time.sleep(0.5)
        except Exception:
            pass
        
        # 2. Click Search
        search_btn = driver.find_element(By.ID, "search")
        driver.execute_script("arguments[0].click();", search_btn)
        
        # 3. Wait for results
        time.sleep(3)
        
        show_div = driver.find_element(By.ID, "show")
        if "无对应学校" in show_div.text:
            result_data["message"] = "官方系统未查到该地址划片信息。"
        else:
            school_items = show_div.find_elements(By.TAG_NAME, "li")
            if school_items:
                result_data["schools"] = [item.text.strip() for item in school_items if item.text.strip()]
                result_data["message"] = f"成功获取到 {len(result_data['schools'])} 个对口学校。"
            else:
                result_data["status"] = "error"
                result_data["message"] = "网页已返回结果，但未能解析到具体学校列表。"
                
    except Exception as e:
        result_data["status"] = "error"
        result_data["message"] = f"自动化操作失败: {str(e)}"
    finally:
        driver.quit()
        
    return result_data


def query_haidian_school(community_name):
    """海淀区：基于17个官方学区名单，引导 Agent 通过搜索确定学区后查询学校"""
    json_path = os.path.join(SCRIPT_DIR, "haidian_districts.json")
    
    if not os.path.exists(json_path):
        return {
            "status": "error",
            "message": "海淀区学区数据文件 haidian_districts.json 未找到。"
        }
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    districts_data = data.get("districts", {})
    available_districts = list(districts_data.keys())

    # 逻辑重构：不再尝试在脚本内用子串匹配小区名（极易出错）
    # 检查输入的 community_name 是否直接就是一个学区名
    if community_name in districts_data:
        info = districts_data[community_name]
        return {
            "district": "海淀",
            "school_district": community_name,
            "status": "success",
            "小学": info.get("小学", []),
            "中学": info.get("中学", []),
            "source": "海淀区 17 学区官方学校名录 (2025)",
            "note": data.get("note", "")
        }

    # 如果不是学区名，则要求 Agent 去搜索
    return {
        "district": "海淀",
        "community": community_name,
        "status": "info_required",
        "message": f"海淀区实行17学区制。为了绝对准确，请不要猜测。请按以下步骤操作：",
        "instruction": [
            f"1. 使用 `web_search` 搜索：'海淀区 {community_name} 属于哪个学区'（上地、中关村、学院路等）。",
            "2. 得到确切学区名后，再次运行本脚本，`--name` 参数直接传入学区名称。",
            "3. 或者直接查阅 `available_districts` 列表中的条目。"
        ],
        "available_districts": available_districts
    }


DISTRICT_MAP = {
    "朝阳": {
        "url": "http://xqcx.bjchyedu.cn/",
        "tips": "朝阳区官方查询系统。输入小区名称或详细地址即可查询对应的小学和初中。"
    },
    "海淀": {
        "url": "https://www.bjhd.gov.cn/kjhd/",
        "tips": "海淀区教育考试中心。包含学区地图和入学政策。建议在‘教育服务’栏目下查找具体的划片查询入口。"
    },
    "东城": {
        "url": "https://www.dcks.org.cn/",
        "tips": "东城区教育招生考试中心。每年4-5月会开通专门的小学入学划片服务系统。"
    },
    "西城": {
        "url": "https://www.xckszx.com/",
        "tips": "西城区教育考试中心。提供学区划分说明和政策文件查询。"
    },
    "丰台": {
        "url": "http://www.bjft.gov.cn/bjft/index/xxgk_list.shtml?q=%E5%AD%A6%E5%8C%BA",
        "tips": "丰台区政府‘政府信息公开’栏目，建议搜索‘学区划片’或‘所属学区’查看最新对照表。"
    },
    "石景山": {
        "url": "http://www.sjsedu.cn/",
        "tips": "石景山区教育委员会。重点关注‘招生考试’或‘政务公开’栏目下的入学方案。"
    },
    "大兴": {
        "url": "https://www.bjdx.gov.cn/ptl/index/index.html",
        "tips": "大兴区人民政府网。在‘教育’或‘办事服务’板块查询义务教育入学政策。"
    },
    "顺义": {
        "url": "http://www.bjshy.gov.cn/bjshy/index/index.html",
        "tips": "顺义区人民政府网，查看教委发布的义务教育阶段入学工作意见及学校招收范围。"
    },
    "房山": {
        "url": "http://www.bjfsh.gov.cn/zwgk/zdly/jy/",
        "tips": "房山区政府重点领域信息公开（教育），发布划片范围和招生简章。"
    },
    "通州": {
        "url": "http://www.bjtzh.gov.cn/bjtz/home/education/index.shtml",
        "tips": "通州区教育信息网，可查询最新的划片范围公告。"
    },
    "昌平": {
        "url": "http://www.bjchp.gov.cn/cpqzf/xxgk22/zdlyxxgk/jyxx6/index.html",
        "tips": "昌平区政府教育公开栏目，通常查看学校发布的招生简章来确认范围。"
    },
    "门头沟": {
        "url": "http://www.bjmtg.gov.cn/bjmtg/zwgk/zdly/jyxx1/index.shtml",
        "tips": "门头沟区政府教育信息公开，查看招生范围和入学政策。"
    },
    "怀柔": {
        "url": "http://www.bjhr.gov.cn/zwgk/zdlyxxgk/jyxx/index.html",
        "tips": "怀柔区政府教育公开。每年会发布城区小学入学划片范围示意图。"
    },
    "密云": {
        "url": "http://www.bjmy.gov.cn/col/col121/index.html",
        "tips": "密云区政府教育公开。重点查看服务片区划分和招生说明。"
    },
    "平谷": {
        "url": "http://www.bjpg.gov.cn/pgqzf/zwgk/zdly/jy13/index.html",
        "tips": "平谷区政府教育公开，发布入学划片 and 学校分布信息。"
    },
    "延庆": {
        "url": "http://www.bjyq.gov.cn/yqzf/zwgk/zdlyxxgk/jy/index.html",
        "tips": "延庆区政府教育信息公开，查看年度义务教育入学工作方案。"
    },
    "经开": {
        "url": "http://kfqgw.beijing.gov.cn/zwgk/zdlyxxgk/jy/",
        "tips": "北京经开区（亦庄）教育信息公开，查询小区服务范围和多校划片说明。"
    }
}

def get_other_district_instruction(district_name):
    """其他区：返回指引信息"""
    source = {
        "url": "http://yjrx.bjedu.cn/",
        "tips": "北京市义务教育入学服务平台（全市统一入口）。您可以在此选择具体区县查看政策。建议手动访问或通过搜索工具确认各区教委的最新发布。"
    }
    
    for key, val in DISTRICT_MAP.items():
        if key in district_name:
            source = val
            break

    return {
        "status": "action_required",
        "district": district_name,
        "official_url": source["url"],
        "message": f"{district_name}的官方划片查询需要家长授权或身份认证（例如登录京学通扫码）。",
        "tips": source["tips"],
        "instruction": "请使用 `browser` 系统工具，引导用户自行在浏览器中打开对应官方网址完成查询验证。"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通过浏览器自动化查询北京各区官方学区")
    parser.add_argument("--district", required=True, help="区县名称（如：朝阳、海淀）")
    parser.add_argument("--name", required=True, help="要查询的详细小区名或地址")
    args = parser.parse_args()

    if "朝阳" in args.district:
        result = query_chaoyang_school(args.name)
    elif "海淀" in args.district:
        result = query_haidian_school(args.name)
    else:
        result = get_other_district_instruction(args.district)
        
    print(json.dumps(result, ensure_ascii=False, indent=2))
