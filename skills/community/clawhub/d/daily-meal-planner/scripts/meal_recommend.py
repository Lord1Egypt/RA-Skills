#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""菜谱推荐引擎 v1.1"""
import sys,random,os,json,argparse
from datetime import datetime
DATA_MIRRORS=[
 "https://github.com/GMMG55/daily-meal-planner/raw/main/scripts",
 "https://cdn.jsdelivr.net/gh/GMMG55/daily-meal-planner@main/scripts"
]  # 移除 ghproxy 第三方镜像，只保留官方源
def _dl(fn):
 p=os.path.join(os.path.dirname(__file__),fn)
 if os.path.exists(p):return True
 for base in DATA_MIRRORS:
  try:
   from urllib.request import urlopen;d=urlopen(f"{base}/{fn}",timeout=15).read()
   with open(p,'wb') as f:f.write(d);return True
  except:continue
 return False
def _lj(fn):
 p=os.path.join(os.path.dirname(__file__),fn)
 if not os.path.exists(p):_dl(fn)
 if os.path.exists(p):
  with open(p,'r',encoding='utf-8-sig') as f:return json.load(f)
 return None
def load_meals_db():
 data=_lj('meals_db_compressed.json');tags=_lj('meals_tags_index.json')or[]
 if not data:return[]
 meals=[]
 for ct,ds in data.items():
  for d in ds:
   d=dict(d);d['meal_type']=ct
   d['tags']=[tags[i]for i in d.get('t',[])if i<len(tags)]if tags else d.get('t',[])
   for k,nk in[('n','name'),('c','cal'),('d','difficulty'),('dsc','desc'),('ing','ingredients'),('stp','steps')]:
    if k in d:d[nk]=d.pop(k)
   d.setdefault('time','30min');d.setdefault('nutrition',{});d.setdefault('seasonal',[]);d.setdefault('regional',[])
   meals.append(d)
 return meals
def load_menu_names():
 data=_lj('menu_names_compressed.json');tags=_lj('tags_index.json')or[]
 if not data:return[]
 out=[]
 for cat,items in data.items():
  for it in items:
   it=dict(it);it['category']=cat
   it['tags']=[tags[i]for i in it.get('t',[])if i<len(tags)]if tags else it.get('t',[])
   for k,nk in[('n','name'),('c','cuisine')]:
    if k in it:it[nk]=it.pop(k)
   out.append(it)
 return out
MEALS_DB=load_meals_db();MENU_NAMES=load_menu_names()
ST={"春":"🌸 春天来啦！肝气旺盛的日子，来点绿叶菜疏通疏通～豆芽菠菜春笋，都是这个季节的限定美味！","夏":"☀️ 炎炎夏日要清凉！瓜果凉菜最解暑，绿豆汤酸梅汤喝起来，凉凉爽爽过一夏～","秋":"🍂 秋天宜润燥！天气渐凉渐干，银耳梨汤润起来，板栗飘香贴秋膘～","冬":"❄️ 冬天宜温补！寒冷的天气需要一点暖意，牛羊肉根茎类，暖胃又滋补~"}
WL={"hot":"炎热","cold":"寒冷","rainy":"雨天","sunny":"晴天","smog":"雾霾","snow":"下雪","windy":"大风","cool":"降温","warm":"升温","humid":"闷热","dry":"干燥"}
WR={0:"周一清淡养胃",1:"周二营养跟上",2:"周三犒劳自己",3:"周四整点好吃的",4:"周五庆祝一下🎉",5:"周末丰盛硬菜",6:"周日懒觉模式"}
MT={"疲惫":["清淡","养胃","高蛋白"],"忙碌":["快手","清淡"],"开心":["硬菜","家常","经典"],"放松":["家常","素食","清淡"],"庆祝":["硬菜","经典","下饭"],"慵懒":["快手","清淡","饱腹"]}
WT={"主食":["饱腹","家常"],"肉":["硬菜","高蛋白"],"素":["素食","清淡"],"汤":["汤品","养胃"],"辣":["川菜","湘菜","下饭"],"清淡":["清淡","素食","凉菜"],"甜":["甜品","养颜"],"小食":["快手","清淡"]}
RM={"北京":["京味","鲁菜"],"上海":["沪菜","江浙"],"重庆":["川菜"],"广东":["粤菜"],"四川":["川菜"],"湖南":["湘菜"],"山东":["鲁菜"],"江苏":["江浙"],"浙江":["江浙"],"福建":["闽菜"],"陕西":["西北"],"新疆":["清真","西北"],"辽宁":["东北菜"],"吉林":["东北菜"],"黑龙江":["东北菜"]}
SD=os.path.dirname(os.path.abspath(__file__));PF=os.path.join(SD,"user_profile.json")
DP={"location":None,"weather":None,"weather_auto":False,"taste":None,"preferred_cuisines":[],"liked_dishes":[],"disliked_dishes":[],"mood":None,"wanted_category":None,"diet_goal":None,"allergies":[],"dislike":[],"last_updated":None}
def load_profile():
 if os.path.exists(PF):
  try:p=json.load(open(PF,"r",encoding="utf-8"));m=DP.copy();m.update(p);return m
  except:pass
 return DP.copy()
def save_profile(pf):
 pf["last_updated"]=datetime.now().strftime("%Y-%m-%d %H:%M")
 try:json.dump(pf,open(PF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
 except:pass
def fetch_weather(city):
 if not city:return None,None
 try:
  import urllib.request
  r=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://wttr.in/{city}?format=j1",headers={"User-Agent":"Mozilla/5.0"}),timeout=6).read().decode())
  c=r["current_condition"][0];t=int(c.get("FeelsLikeC",0));d=c.get("weatherDesc",[{}])[0].get("value","").lower()
  if"snow"in d:code="snow"
  elif"rain"in d or"drizzle"in d:code="rainy"
  elif"fog"in d or"mist"in d or"haze"in d:code="smog"
  elif"cloud"in d:code="sunny"if t>18 else"cold"
  elif"sunny"in d or"clear"in d:code="sunny"
  else:code="hot"if t>28 else("cold"if t<10 else"sunny")
  return code,f"{WL.get(code,'')} {t}°C"
 except:return None,None
def get_regional_tags(loc):
 if not loc:return[]
 for k,v in RM.items():
  if k in loc:return v
 return[]
def get_season():
 m=datetime.now().month
 if m in[3,4,5]:return"春"
 if m in[6,7,8]:return"夏"
 if m in[9,10,11]:return"秋"
 return"冬"
WB={"hot":{"清淡":2,"凉菜":1,"硬菜":-1},"humid":{"清淡":2,"凉菜":1,"硬菜":-1},"cold":{"家常":1,"汤品":1,"清淡":1},"cool":{"家常":1,"汤品":1,"清淡":1},"snow":{"家常":1,"汤品":1,"清淡":1},"rainy":{"汤品":2,"养胃":2,"清淡":1},"sunny":{"清淡":1,"凉菜":1},"smog":{"清淡":2,"养胃":1},"warm":{"清淡":1,"凉菜":1,"润燥":2},"dry":{"清淡":1,"凉菜":1,"润燥":2},"windy":{"家常":1,"汤品":1}}
WR_DESC={"hot":"清热解腻","humid":"清热解腻","cold":"暖身滋补","cool":"暖身滋补","snow":"暖身滋补","rainy":"雨天暖汤","sunny":"晴天清爽","smog":"护肺清肺","warm":"升温清淡","dry":"干燥润肺","windy":"大风暖身"}
def score_meal(meal,season,wd,weather,used,regional=[],profile=None):
 name=meal.get('name','')
 if name in used:return -999,[]
 s=0;rs=[];tags=meal.get("tags",[])
 # 季节
 if season in meal.get("seasonal",[]):s+=3;rs.append("应季食材")
 # 周几
 if wd==4:
  if"硬菜"in tags:s+=2
  rs.append("周五庆祝")
 elif wd in[0,1,2]:
  if"清淡"in tags or"快手"in tags:s+=1
 elif wd in[5,6]:
  if"硬菜"in tags or"家常"in tags:s+=2;rs.append("周末丰盛")
 # 天气
 if weather in WB:
  for tag,bonus in WB[weather].items():
   if tag in tags:s+=bonus
  rdesc=WR_DESC.get(weather,"");rs.append(rdesc)
 # 地域（用户所在地 → 菜系标签加权）
 loc_regional=meal.get("regional",[])
 if regional and loc_regional:
  match=set(loc_regional)&set(regional)
  if match:s+=2.5;rs.append("本地风味")
 # 口味偏好（profile里的wanted_category）
 if profile:
  wanted=profile.get("wanted_category","")
  if wanted in WT:
   for t in WT[wanted]:
    if t in tags:s+=1.2
  preferred=profile.get("preferred_cuisines",[])
  if preferred:
   for pc in preferred:
    if pc in tags or pc.replace("菜","")in name:s+=1.5;rs.append("偏好"+pc)
 # 心情加权
 mood=profile.get("mood","")if profile else""
 if mood in MT:
  for t in MT[mood]:
   if t in tags:s+=1.5
 # 之前喜欢的菜
 liked=profile.get("liked_dishes",[])if profile else[]
 if liked and name in liked:s+=2;rs.append("你喜欢的")
 # 厌恶的菜（扣分）
 disliked=profile.get("disliked_dishes",[])if profile else[]
 if disliked and any(d in name or d in",".join(tags)for d in disliked):s-=5
 # 大幅增大随机：让结果更有多样性
 s+=random.uniform(0.5,4.0)
 return s,rs
def get_side(main,mt,season,used):
 pools=["午餐","晚餐"]if mt in["午餐","晚餐"]else[mt]
 sides=[m for p in pools for m in MEALS_DB if m.get("meal_type")==p and any(t in m.get("tags",[])for t in["清淡","素食","凉菜","快手"])and m['name']not in used and m['name']!=main['name']]
 if season=="夏":
  ss=[m for m in sides if"凉菜"in m.get("tags",[])]
  if ss:sides=ss
 return random.choice(sides[:6])if sides else None
def get_soup(mt,season,used):
 if mt=="早餐":
  bp=[m for m in MEALS_DB if m.get("meal_type")=="早餐"and m['name']not in used and m['name']in["小米粥","蔬菜粥","蒸蛋羹","牛奶燕麦"]]
  return random.choice(bp)if bp else None
 pools=["午餐","晚餐"]if mt in["午餐","晚餐"]else[mt]
 soups=[m for p in pools for m in MEALS_DB if m.get("meal_type")==p and any(t in m.get("tags",[])for t in["汤品","养胃","清淡"])and m['name']not in used]
 return random.choice(soups[:8])if soups else None
def recommend_smart(meal_time=None,weather=None,location=None,profile=None,count=3,exclude_names=None):
 season=get_season();wd=datetime.now().weekday();wd_name=["周一","周二","周三","周四","周五","周六","周日"][wd]
 if meal_time is None:meal_time="午餐"
 liked=profile.get("liked_dishes",[])if profile else[]
 disliked=profile.get("disliked_dishes",[])if profile else[]
 mood=profile.get("mood","")if profile else""
 wanted=profile.get("wanted_category","")if profile else""
 regional=get_regional_tags(location)if location else[]
 # 主池：MEALS_DB 完整菜谱（按餐次过滤）
 pool_full=[m for m in MEALS_DB if m.get("meal_type")==meal_time]
 # 扩展池：MENU_NAMES 全部菜单名（不限餐次，只要有对应tag就算）
 def match_mt(m):
   tags=m.get("tags",[])
   mt_tags={"午餐":["午餐","主食","家常"],"晚餐":["晚餐","硬菜","家常"],"早餐":["早餐","饱腹"],"下午茶":["甜品","小吃","下午茶"],"夜宵":["夜宵","小吃"]}
   allowed=mt_tags.get(meal_time,["午餐"])
   return any(t in allowed or t in["家常","素食","清淡"]for t in tags)
 pool_extra=[{"name":m["name"],"tags":m.get("tags",[]),"category":m.get("category",""),"cuisine":m.get("cuisine",""),"_menu_only":True}for m in MENU_NAMES if match_mt(m)]
 pool=pool_full+pool_extra
 used=list(exclude_names or[]);results=[]
 def ok(m):
   n=m.get("name","")
   return not any(d in n or d in",".join(m.get("tags",[]))for d in disliked)
 def pick(m,reason):
   u2=used+[m['name']]
   if not m.get("_menu_only"):
    side=get_side(m,meal_time,season,u2);soup=get_soup(meal_time,season,u2+([side['name']]if side else[]))
    results.append((m,reason,side,soup))
   else:
    results.append((m,reason,None,None))
   used.append(m['name'])
 scored=[]
 for m in pool:
  if not ok(m):continue
  s,rs=score_meal(m,season,wd,weather,used,regional,profile)
  scored.append((s,m,rs))
 scored.sort(key=lambda x:-x[0])
 if scored:
  # 增强版原因池：评分返回的rs可能很干，这里补全成有血有肉的自然语言
  ENHANCED={
   "周五庆祝":"周五啦！辛苦了一周，该好好犒劳自己~","周末丰盛":"周末时光正好，来点硬菜凑个热闹~","应季食材":"当季限定鲜货，大自然的馈赠~",
   "清淡养胃":"清淡不腻，肠胃无负担~","清热解腻":"清热解腻，夏天吃正合适~","雨天暖汤":"雨天配热汤，暖到心坎里~",
   "晴天清爽":"晴天配清爽菜，心情也跟着好~","你喜欢的菜":"你之前说喜欢这个~","本地风味":"家乡风味，最对味~",
   "高蛋白":"优质蛋白补充，吃出好状态~","快手方便":"简单快手，十分钟搞定~","养胃":"温和养胃，吃着舒服~",
   "经典之选":"经典搭配，怎么吃都不腻~","养颜美容":"好吃又养颜，赞~",
  }
  def humanize_reason(rs):
   parts=[ENHANCED.get(r,r)for r in rs if r]
   if not parts:
    day_bless={0:"新的一周从轻食开始~",1:"周二营养要跟上~",2:"周三给自己加点能量~",3:"周四快到周末啦~",4:"周五庆祝一下！",5:"周末就是要吃好~",6:"周日悠闲时光~"}
    parts=[day_bless.get(wd,"好好吃饭~")]
   # 随机加一句小彩蛋
   extras=["心动不如行动！","好吃不解释~","绝对不会踩雷~","墙裂推荐~","吃完还想再来~","营养又美味~","简单却不普通~"]
   if random.random()<0.6:parts.append(random.choice(extras))
   return"，".join(parts[:2])
 if scored:
  b=scored[0];reason=humanize_reason(b[2]);pick(b[1],f"📌 {reason}")
 sp=[m for m in pool if m['name'] not in used and ok(m)and season in m.get("seasonal",[])]
 if not sp:sp=[m for m in pool if m['name'] not in used and ok(m)]
 if sp:
  r=f"🌿 时令鲜货！{season}季的菜最嫩最香，可别错过~";pick(random.choice(sp),r)
 rem=[m for m in pool if m['name'] not in used and ok(m)]
 if rem:
  pick(random.choice(rem),"🎲 猜你会喜欢！试试这道，说不定有新发现~")
 return results[:count],wd_name
def fmt_results(results,wd_name,season,meal_time="午餐",weather=None,location=None):
 icon={"早餐":"🌅","午餐":"☀️","晚餐":"🌙","下午茶":"🫖","夜宵":"🌃"}.get(meal_time,"🍽️");lines=[]
 for i,(meal,reason,side,soup)in enumerate(results,1):
  lines+=[f"  {'─'*32}",f"  {icon} 推荐{i}  {meal['name']}"]
  if meal.get("_menu_only"):
   tags=meal.get("tags",[]);cat=meal.get("category","");cuisine=meal.get("cuisine","")
   # 分类/菜系 + 标签（合并到一行）
   parts=[]
   if cuisine:parts.append(cuisine)
   if cat:parts.append(cat)
   tag_str=" ".join("#"+t for t in tags[:4])if tags else""
   if parts and tag_str:lines.append(f"  🏷️ {' | '.join(parts)} · {tag_str}")
   elif parts:lines.append(f"  🏷️ {' | '.join(parts)}")
   elif tag_str:lines.append(f"  🏷️ {tag_str}")
   # 推荐原因
   lines.append("  💡 "+reason)
   # 提示用户可以搜索做法
   lines.append("  🌐 回复「搜 "+meal['name']+"」查找做法，或告诉我想看哪道菜的详情~")
  else:
   cal=meal['cal']+(side['cal']if side else 0)+(soup['cal']if soup else 0)
   lines+=[f"  📝 {meal['desc']}",f"  💡 {reason}",f"  🔥 {cal}kcal  ⏱ {meal['time']}  难度: {meal['difficulty']}"]
   np=[f"{k}:{v}"for k,v in meal.get('nutrition',{}).items()if k in['蛋白质','维C','铁','钙']]
   if np:lines.append(f"  📊 {' | '.join(np)}")
   if meal.get('regional'):lines.append(f"  🏠 {','.join(meal['regional'])}")
   lines.append(f"  🥗 食材: {','.join(meal['ingredients'][:4])}")
   if side:lines.append(f"  🥬 +配: {side['name']}（{side['cal']}kcal）")
   if soup:lines.append(f"  🍲 +汤/饭: {soup['name']}（{soup['cal']}kcal）")
 lines+=[f"  {'─'*32}",f"  💡 回复「要」或「1/2/3」查看详细做法 👨‍🍳  ·  「换个」换一批"]
 return"\n".join(lines)
def _motivation(wd, wd_name, weather, loc, top_meal):
    today=datetime.now();days_to=None;holiday=""
    # 尝试从 API 实时获取节假日（失败则跳过）
    try:
        import urllib.request,json
        year=today.year
        url=f"https://date.nager.at/api/v3/PublicHolidays/{year}/CN"
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        data=json.loads(urllib.request.urlopen(req,timeout=5).read().decode())
        holidays=[(datetime.strptime(h["date"],"%Y-%m-%d"),h["localName"])for h in data]
        for h,d in holidays:
            if h>=today:days_to=(h-today).days;holiday=d;break
    except:pass  # API 失败时不影响主功能
    mp="来盘"+top_meal+"开启新的一周" if top_meal else "好好吃一顿"
    dm={0:"周一到，开工啦！",4:"周五到，犒劳自己~",5:"周末来，睡懒觉吃好的~",6:"周日悠闲时光~",1:"周二新开始，继续加油~",2:"周三小节点，撑过去~",3:"周四到，周末就来了~"}
    dm2=dm.get(wd,"好好吃~")
    if wd==0:
     if days_to is not None and days_to<=7:dm2+=" 再坚持"+str(days_to)+"天就放假啦~"
     elif days_to is not None and days_to<=30:dm2+=" 距离"+holiday+"还有"+str(days_to)+"天~"
    wm={"hot":"热得很~","sunny":"大晴天，万里无云~","cold":"外面冷嗖嗖的~","rainy":"雨天窝家暖暖的~","smog":"雾霾天，少出门~","snow":"下雪天最浪漫~","warm":"升温啦~","cool":"降温了~","dry":"干燥得很~","humid":"闷热潮湿~","windy":"大风呼呼~"}.get(weather,"")
    parts=[p for p in[dm2,wm]if p]
    if len(parts)==2:msg=parts[0]+"，"+parts[1]+"，"
    elif parts:msg=parts[0]+"，"
    else:msg=""
    msg+=mp+"～加油💪"
    return "  "+msg

def weekly_context():
    """收集一周菜谱规划所需的上下文，输出 JSON 供 AI 使用"""
    season = get_season()
    pf = load_profile()
    loc = pf.get('location', '')
    w_code, w_desc = fetch_weather(loc) if loc else (None, None)
    w = w_code or pf.get('weather', '')
    # 收集菜谱库
    dishes = []
    for m in MEALS_DB:
        dishes.append({'name': m.get('name',''), 'tags': m.get('tags',[]), 'regional': m.get('regional',[]), 'seasonal': m.get('seasonal',[]), 'cal': m.get('cal',''), 'desc': m.get('desc',''), 'time': m.get('time',''), 'difficulty': m.get('difficulty',''), 'ingredients': m.get('ingredients',[]), 'meal_type': m.get('meal_type','')})
    for m in MENU_NAMES:
        dishes.append({'name': m.get('name',''), 'tags': m.get('tags',[]), 'cuisine': m.get('cuisine',''), 'category': m.get('category','')})
    seen = set(); unique = []
    for d in dishes:
        if d['name'] and d['name'] not in seen:
            seen.add(d['name']); unique.append(d)
    today = datetime.now(); weekday = today.weekday()
    from datetime import timedelta
    monday = today - timedelta(days=weekday)
    days = [{'date': (monday + timedelta(days=i)).strftime('%m-%d'), 'weekday': ['周一','周二','周三','周四','周五','周六','周日'][i], 'is_weekend': i >= 5} for i in range(7)]
    ctx = {
        'season': season, 'location': loc,
        'weather_code': w, 'weather_desc': w_desc,
        'today': today.strftime('%Y-%m-%d'), 'today_weekday': weekday,
        'profile': {k: pf.get(k) for k in ['preferred_cuisines','mood','diet_goal','disliked_dishes','allergies']},
        'week_days': days,
        'dish_pool': unique[:300],
        'pool_size': len(unique)
    }
    print(json.dumps(ctx, ensure_ascii=False, indent=2))

def fmt_daily(results,wd_name,season,meal_time,weather,profile,wd_detail=None):
 loc=profile.get("location","");wl_desc=WL.get(weather,"")if weather else""
 loc_str=f"📍{loc} "if loc else""
 weather_str=f"{wl_desc} · "if wl_desc and wl_desc!="sunny"else""
 wd=datetime.now().weekday()
 mot=_motivation(wd,wd_name,weather,loc,results[0][0]["name"]if results else"")
 h=f"\n🍽️ {loc_str}今日{meal_time}推荐  {weather_str}{wd_name} · {season}季\n{ST.get(season,'')}\n{mot}"
 extras=[]
 if profile.get("diet_goal"):extras.append({"减肥":"低卡🎯","增肌":"高蛋白💪","养生":"滋补🍵","保持":"均衡⚖️"}.get(profile['diet_goal'],profile['diet_goal']))
 if profile.get("preferred_cuisines"):extras.append(f"偏好: {','.join(profile['preferred_cuisines'])}")
 if profile.get("mood"):extras.append(f"心情: {'😊💼😫🧘🎉😴'.encode().decode()}") # simplified
 if extras:h+="\n"+"  ".join(extras)
 body=fmt_results(results,wd_name,season,meal_time,weather,loc)
 hints=[]
 if not profile.get("location"):hints.append("📍 你在哪个城市？")
 if not profile.get("mood"):hints.append("😊 心情？开心/忙碌/疲惫/放松/庆祝")
 if not profile.get("wanted_category"):hints.append("🍽️ 想吃？主食/肉/素/汤/辣/清淡/甜")
 if not profile.get("preferred_cuisines"):hints.append("🍜 偏好菜系？川菜/粤菜/鲁菜/江浙…")
 if not profile.get("diet_goal"):hints.append("🎯 饮食目标？减肥/增肌/养生")
 ask=""
 if hints:ask="\n\n💬 告诉我这些，推荐更精准：\n"+"\n".join(f"   {h}"for h in hints)+"\n💡 一句话搞定：「北京，心情不错，想吃辣的，川菜」以后自动用～"
 return h+body+ask
def fmt_detail(meal):
 lines=[f"  🍽️ {meal['name']}",f"     💡 {meal['desc']}",f"     🔥 ~{meal['cal']}kcal | ⏱ {meal['time']} | {meal['difficulty']}"]
 if meal.get('nutrition'):lines.append(f"     💊 {' | '.join(f'{k}:{v}'for k,v in meal['nutrition'].items())}")
 lines+=[f"     🥬 {', '.join(meal['ingredients'])}",f"     🏷️ {', '.join(meal['tags'])}"]
 if meal.get('steps'):lines+=["     📝 做法:"]+[f"       {i+1}. {s}"for i,s in enumerate(meal['steps'])]
 return"\n".join(lines)
if __name__=="__main__":
 pa=argparse.ArgumentParser();pa.add_argument("mode",help="daily/weekly/search/detail");pa.add_argument("args",nargs="*");pa.add_argument("--meal","-m",default=None);pa.add_argument("--weather","-w",default=None);pa.add_argument("-n","--count",type=int,default=3)
 a=pa.parse_args();q=" ".join(a.args);mt=a.meal
 cn={"breakfast":"早餐","lunch":"午餐","dinner":"晚餐","supper":"夜宵","afternoon_tea":"下午茶"}
 if mt in cn:mt=cn[mt]
 if a.mode=="daily":
  if not mt:mt="晚餐"if datetime.now().hour>=17 else"午餐"
  for kw in["早餐","午餐","晚餐","夜宵"]:
   if kw in q:mt=kw;break
  season=get_season();wd=datetime.now().weekday();wn=["周一","周二","周三","周四","周五","周六","周日"][wd];pf=load_profile()
  w=wdd=None
  if pf.get("location"):w,wdd=fetch_weather(pf["location"])
  if not w:w=a.weather or pf.get("weather")
  if w:pf["weather"]=w;pf["weather_auto"]=True;save_profile(pf)
  # 输出上下文 JSON 供 AI 智能推荐
  dishes=[]
  for m in MEALS_DB:
    dishes.append({'name':m.get('name',''),'tags':m.get('tags',[]),'regional':m.get('regional',[]),'seasonal':m.get('seasonal',[]),'cal':m.get('cal',''),'desc':m.get('desc',''),'time':m.get('time',''),'difficulty':m.get('difficulty',''),'ingredients':m.get('ingredients',[]),'meal_type':m.get('meal_type','')})
  for m in MENU_NAMES:
    dishes.append({'name':m.get('name',''),'tags':m.get('tags',[]),'cuisine':m.get('cuisine',''),'category':m.get('category','')})
  seen=set();unique=[]
  for d in dishes:
    if d['name'] and d['name'] not in seen:seen.add(d['name']);unique.append(d)
  ctx={'mode':'daily','meal_time':mt,'season':season,'weekday':wd,'weekday_name':wn,'is_weekend':wd>=5,'location':pf.get('location',''),'weather_code':w,'weather_desc':wdd,'today':datetime.now().strftime('%Y-%m-%d'),'profile':{k:pf.get(k) for k in['preferred_cuisines','mood','diet_goal','disliked_dishes','allergies','wanted_category']},'dish_pool':unique[:300],'pool_size':len(unique)}
  print(json.dumps(ctx,ensure_ascii=False,indent=2))
 elif a.mode=="detail":
  if not q:print("用法: python meal_recommend.py detail <菜名>");sys.exit(1)
  found=[m for m in MEALS_DB if q in m['name']or m['name']in q]
  if found:
   print("\n".join(fmt_detail(m)for m in found))
  else:
   menu_hit=[m for m in MENU_NAMES if q in m['name']or m['name']in q]
   if menu_hit:
    lines=[]
    for m in menu_hit[:3]:
     tags=" ".join("#"+t for t in m.get('tags',[])[:5])
     cuisine=m.get('cuisine','')
     lines.append("  🍽️  "+m['name'])
     if cuisine:lines.append("     🏷️ "+cuisine+(" | "+tags if tags else""))
     elif tags:lines.append("     🏷️ "+tags)
     lines.append("     💡 全网搜索「"+m['name']+" 菜谱」查看做法，或让我 AI 生成原创菜谱~")
     lines.append("")
    print("\n".join(lines).strip())
   else:
    print("未找到「"+q+"」，可全网搜索「"+q+" 菜谱」或让我 AI 生成~")
 elif a.mode=="search":
  if not q:print("用法: python meal_recommend.py search <关键词>");sys.exit(1)
  pf=load_profile();season=get_season();wd=datetime.now().weekday();wn=[WR.get(0,''),WR.get(1,''),WR.get(2,''),WR.get(3,''),WR.get(4,''),WR.get(5,''),WR.get(6,'')][wd]
  w=wdd=None
  if pf.get("location"):w,wdd=fetch_weather(pf["location"])
  if not w:w=a.weather or pf.get("weather") or "sunny"
  kws=q.split()
  # 检测餐次类型
  meal_kws={"早餐":["早餐","早茶"],"午餐":["午餐","午饭"],"晚餐":["晚餐","晚饭"],"下午茶":["下午茶","茶点"],"夜宵":["夜宵","宵夜"]}
  sn={"早餐":"早餐系列","午餐":"午餐套餐","晚餐":"家常菜","下午茶":"甜品小吃","夜宵":"小吃"}
  detected_mt=None
  for mt,kws2 in meal_kws.items():
   if any(kw in q for kw in kws2):detected_mt=mt;break
  # 如果检测到精确餐次，直接从对应分类取，不用模糊搜索
  if detected_mt:
   cm=[m for m in MEALS_DB if m.get('meal_type')==detected_mt]
   # mm 只取同分类的菜单名（不混用关键词搜索）
   sn_key=sn.get(detected_mt,'')
   mm=[m for m in MENU_NAMES if m.get('category')==sn_key]if sn_key else[]
  else:
   cm=[m for m in MEALS_DB if any(k.lower()in m['name'].lower()or k in",".join(m.get('tags',[]))for k in kws)]
   mm=[m for m in MENU_NAMES if any(k.lower()in m['name'].lower()or k in",".join(m.get('tags',[]))for k in kws)]
   mm=[m for m in mm if m['name']not in set(x['name']for x in cm)]
  EXCLUDE_TAGS={"下午茶":["硬菜","大荤","川菜","湘菜"],"早餐":["硬菜","大荤","川菜","湘菜"]}
  exclude_tags=EXCLUDE_TAGS.get(detected_mt,[])
  if exclude_tags:
   cm=[m for m in cm if not any(t in m.get('tags',[])for t in exclude_tags)]
   mm=[m for m in mm if not any(t in m.get('tags',[])for t in exclude_tags)]
  # 合并：MEALS_DB项目在前， MENU_NAMES只显示名称
  combined=cm[:8]+[{"name":m['name'],"category":m.get('category',''),"tags":m.get('tags',[]),"_menu_only":True}for m in mm[:12]]
  if not combined:print(f"未找到「{q}」相关菜品");sys.exit(0)
  # 复用推荐逻辑评分
  used=[];results=[]
  regional=get_regional_tags(pf.get("location",""))
  liked=pf.get("liked_dishes",[]);disliked=pf.get("disliked_dishes",[]);mood=pf.get("mood","");wanted=pf.get("wanted_category","")
  def ok(m):return not any(d in m.get("name","")or d in",".join(m.get("tags",[]))for d in disliked)
  def boost(m):
   b=0;tags=m.get("tags",[])
   if mood in MT:
    for t in MT[mood]:
     if t in tags:b+=1.5
   if wanted in WT:
    for t in WT[wanted]:
     if t in tags:b+=1
   return b
  scored=[]
  for m in combined:
   if not ok(m):continue
   s=0;rs=[]
   if not m.get("_menu_only"):
    s,rs=score_meal(m,season,wd,w,used)
   if liked and m.get("name")in liked:s+=2;rs.append("你喜欢的菜")
   if regional and m.get("regional")and set(m["regional"])&set(regional):s+=2;rs.append("本地风味")
   s+=boost(m);scored.append((s,m,rs))
  scored.sort(key=lambda x:-x[0])
  # 分配推荐类型（循环覆盖所有结果）
  type_cycle=["📌 综合推荐：","🌿 时令之选：","🎲 随机惊喜："]
  # 精细化推荐原因
  REASON_TIPS={"甜":"甜品最治愈，治愈你的小确丧~","清热":"清热解暑，告别夏天黏腻感~","经典":"经典之选，吃过都说好~","广式":"广式风味，细腻又讲究~","养颜":"好吃又美颜，爱自己多一点~","饱腹":"吃饱不想家，性价比超高~","快手":"十分钟搞定，懒人福音~","养胃":"温和不刺激，胃舒服了人舒坦~","川菜":"香辣过瘾，下饭一绝~","粤菜":"清淡鲜美，原汁原味超会吃~","鲁菜":"咸香正宗，北方胃的最爱~","江浙":"甜中带鲜，江南婉约风味~","东北菜":"份量实在，吃饱吃好不将就~","家常":"家的味道，熟悉的温暖~","素食":"轻盈无负担，身心都舒畅~","硬菜":"大鱼大肉硬菜撑场~","汤品":"热汤暖胃又营养~","下饭":"一口下去饭遭殃~"}
  lines=[]
  loc_desc=f"📍 {pf.get('location','')}"if pf.get("location")else""
  weather_desc=WL.get(w,"")if w else""
  header_parts=[p for p in[loc_desc,weather_desc,wn,f"{season}季"]if p]
  icon="🫖"if"茶"in q or"下午茶"in q else("🌅"if"早餐"in q else("☀️"if"午餐"in q else("🌙"if"晚餐"in q else"🍽️")))
  lines.append(f"\n{icon} 查询结果  {' · '.join(header_parts)}")
  lines.append(ST.get(season,""))
  for i,(s,m,rs)in enumerate(scored[:6]):
   # 精细化推荐原因
   tag_reason=""
   if m.get('tags'):
    for t in m['tags']:
     if t in REASON_TIPS:tag_reason=REASON_TIPS[t];break
   base=type_cycle[i%len(type_cycle)]
   extras=[]
   if rs:extras=[r for r in rs if r not in["应季食材","周五庆祝","周末丰盛","本地风味","你喜欢的菜"]]
   reason=base+(tag_reason if tag_reason else("，".join(extras)if extras else"精选推荐"))
   lines.append(f"  {'─'*32}")
   if m.get("_menu_only"):
    lines.append(f"  {icon.replace(' ','')} {i+1}. {m['name']}")
    lines.append(f"     🏷️ {' '.join(f'#{t}'for t in m.get('tags',[])[:3])} [{m.get('category','')}]")
    lines.append(f"     💡 {reason}")
   else:
    lines.append(f"  {icon.replace(' ','')} {i+1}. {m['name']}")
    lines.append(f"     📝 {m.get('desc','暂无描述')}")
    lines.append(f"     💡 {reason}")
    cal=m.get('cal',0);lines.append(f"     🔥 {cal}kcal  ⏱ {m.get('time','30min')}  难度: {m.get('difficulty','中')}")
    ing=m.get('ingredients',[]);lines.append(f"     🥬 食材: {','.join(ing[:4])}")
  lines.append(f"  {'─'*32}")
  lines.append("\n💡 回复「要」或「1/2/3」查看详细做法 👨‍🍳  ·  「换个」换一批")
  print("\n".join(lines))
 elif a.mode=="weekly":
  print(weekly_context())
 else:print(f"未知模式: {a.mode}，支持: daily/weekly/search/detail")
