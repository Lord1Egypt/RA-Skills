"""Family Finance Manager - Routing Engine"""
from engine.types import (FamilyFinanceRequest, FinancialAnalysisReport, SavingsGoalPlan,
    InsuranceRecommendation, RiskWarningReport, FinancialHealthReport)

def run_family_finance_engine(request: FamilyFinanceRequest) -> dict:
    action = request.action
    if action == "analyze": return analyze_financial_health(request)
    elif action == "goal-plan": return plan_savings_goal(request)
    elif action == "insurance": return recommend_insurance(request)
    elif action == "risk-warning": return generate_risk_warning(request)
    elif action == "health-report": return generate_health_report(request)
    else: return {"error": f"Unknown action: {action}"}

def analyze_financial_health(request):
    report = FinancialAnalysisReport()
    mi = request.monthly_income
    me = request.get_total_monthly_expenses()
    ms = mi - me
    sr = (ms / mi * 100) if mi > 0 else 0
    report.income_expense = {"monthlyIncome": mi, "monthlyExpenses": me, "monthlySavings": ms,
        "savingsRate": round(sr, 2), "expenseBreakdown": request.monthly_expenses.copy(),
        "recommendations": _exp_rec(sr, request.monthly_expenses)}
    ta = request.get_total_assets(); tl = request.get_total_liabilities()
    report.net_worth = {"totalAssets": ta, "totalLiabilities": tl, "netWorth": ta-tl,
        "assetsComposition": {"liquid": request.assets.get("liquid",0), "investments": request.assets.get("investments",0), "property": request.assets.get("property",0), "other": request.assets.get("other",0)}}
    efm = (request.assets.get("liquid",0)/me) if me>0 else 0
    ir = (request.assets.get("investments",0)/ta*100) if ta>0 else 0
    mdp = tl * 0.01
    dti = (mdp/mi*100) if mi>0 else 0
    report.ratios = {"debtToIncome": round(dti,2), "emergencyFundMonths": round(efm,1), "investmentRatio": round(ir,2)}
    report.suggestions = _gen_sug(request, sr, dti, efm)
    return report.to_dict()

def plan_savings_goal(request):
    if not request.goals: return {"error": "No financial goal provided"}
    goal = request.goals[0]; plan = SavingsGoalPlan(goal)
    cs = request.assets.get("liquid",0) + request.assets.get("investments",0)
    ar = 0.05; mr = ar/12; nm = goal.years * 12
    if mr>0: mreq = goal.amount * mr / ((1+mr)**nm - 1)
    else: mreq = goal.amount / nm
    plan.monthly_required = round(mreq,2); plan.yearly_required = round(mreq*12,2)
    plan.current_progress = cs; plan.completion_percentage = round((cs/goal.amount)*100,2) if goal.amount>0 else 0
    for i in [1,2,3,5]:
        if i <= goal.years:
            months = i*12; ma = mreq*months+cs
            plan.milestones.append({"month": months, "amount": round(ma,2), "description": f"第{i}年里程碑：积累至{ma/10000:.1f}万元"})
    risk = request.risk_profile
    if risk=="conservative": plan.investment_advice=["建议配置低风险理财产品，如定期存款、国债","银行理财产品的预期年化收益约3-4%","保持50%以上的低风险资产配置"]
    elif risk=="moderate": plan.investment_advice=["建议股债平衡配置，股票类50%，债券类50%","可考虑定投指数基金，分散市场风险","预期年化收益约5-7%"]
    else: plan.investment_advice=["可适当提高权益类资产配置至70-80%","考虑分散投资A股、港股、美股市场","预期年化收益约7-10%，但波动较大"]
    mi = request.monthly_income; me = request.get_total_monthly_expenses(); ms = mi - me
    if mreq <= ms*0.5: plan.risk_assessment = f"目标可实现，风险较低。当前每月可储蓄{ms:.0f}元，目标每月需{mreq:.0f}元，占储蓄能力的{mreq/ms*100:.0f}%。"
    elif mreq <= ms*0.8: plan.risk_assessment = "目标实现有一定压力，需要严格执行储蓄计划。建议调整支出或延长目标时间。"
    else: plan.risk_assessment = "目标实现难度较大，建议降低目标金额或延长实现时间，或增加收入来源。"
    return plan.to_dict()

def recommend_insurance(request):
    rec = InsuranceRecommendation()
    ai = request.family.get("annualIncome", request.monthly_income*12)
    el = request.insurance.get("life",0); eh = request.insurance.get("health",0)
    rl = ai*10; rec.coverage_gaps["life"] = max(0, rl-el)
    rh = ai*3; rec.coverage_gaps["health"] = max(0, rh-eh)
    rd = ai*0.6; rec.coverage_gaps["disability"] = rd
    rc = ai*1.5; rec.coverage_gaps["criticalIllness"] = rc
    rec.total_recommended_coverage = rec.coverage_gaps["life"]+rec.coverage_gaps["health"]+rec.coverage_gaps["disability"]+rec.coverage_gaps["criticalIllness"]
    if rec.coverage_gaps["life"]>0: rec.recommendations.append({"type":"定期寿险","priority":"high","reason":f"家庭经济支柱需要充足的寿险保障，建议保额覆盖{rl/10000:.0f}万元","estimatedPremium": round(rec.coverage_gaps["life"]*0.001,0)})
    if rec.coverage_gaps["health"]>0: rec.recommendations.append({"type":"百万医疗险","priority":"high","reason":"补充社保不足，覆盖高额医疗费用","estimatedPremium": 300})
    if rec.coverage_gaps["criticalIllness"]>ai*0.5: rec.recommendations.append({"type":"重疾险","priority":"medium","reason":"重大疾病可能导致收入中断，需要重疾保障","estimatedPremium": round(rec.coverage_gaps["criticalIllness"]*0.03,0)})
    for m in request.members:
        if m.role in ["self","spouse"] and m.age<50: rec.recommendations.append({"type":f"{m.name}的意外险","priority":"medium","reason":"家庭主要收入来源，建议配置意外险","estimatedPremium": 150})
    rec.budget_considerations=["保险预算建议为年收入的5-10%","优先配置保障型保险，再考虑储蓄型","定期检视保险配置，随家庭情况变化调整"]
    return rec.to_dict()

def generate_risk_warning(request):
    report = RiskWarningReport()
    mi = request.monthly_income; me = request.get_total_monthly_expenses(); ms = mi-me
    tl = request.get_total_liabilities(); la = request.assets.get("liquid",0)
    if mi>0:
        sr = ms/mi
        if sr<0.1: report.risk_factors.append({"factor":"储蓄率过低","level":"high","description":f"当前储蓄率仅{sr*100:.0f}%，低于10%，财务积累能力不足","mitigation":"建议控制非必要支出，将储蓄率提升至20%以上"})
        elif sr<0.2: report.risk_factors.append({"factor":"储蓄率偏低","level":"medium","description":f"当前储蓄率{sr*100:.0f}%，有提升空间","mitigation":"可通过优化支出结构提高储蓄率"})
    if me>0:
        efm = la/me
        if efm<3: report.risk_factors.append({"factor":"紧急备用金不足","level":"high","description":f"当前紧急备用金仅够{efm:.1f}个月，低于3个月标准","mitigation":"建议优先建立3-6个月的紧急备用金"})
        elif efm<6: report.risk_factors.append({"factor":"紧急备用金偏低","level":"medium","description":f"当前紧急备用金约{efm:.1f}个月，建议提升至6个月","mitigation":"逐步增加流动资产储备"})
    if mi>0 and tl>0:
        md = tl*0.01; dr = md/mi
        if dr>0.5: report.risk_factors.append({"factor":"负债率过高","level":"critical","description":f"负债收入比{dr*100:.0f}%，超过50%危险线","mitigation":"立即制定债务还款计划，优先偿还高息债务"})
        elif dr>0.36: report.risk_factors.append({"factor":"负债率偏高","level":"high","description":f"负债收入比{dr*100:.0f}%，处于警戒区间","mitigation":"注意债务管理，避免进一步增加负债"})
    er = me/mi if mi>0 else 1
    if er>0.9: report.risk_factors.append({"factor":"支出占比过高","level":"high","description":f"支出占收入{er*100:.0f}%，几乎没有储蓄空间","mitigation":"必须审视并削减非必要支出"})
    hc = sum(1 for rf in report.risk_factors if rf["level"] in ["high","critical"])
    if hc>=3: report.overall_risk_level="critical"
    elif hc>=2: report.overall_risk_level="high"
    elif hc>=1: report.overall_risk_level="medium"
    else: report.overall_risk_level="low"
    if report.overall_risk_level in ["high","critical"]: report.immediate_actions.extend(["立即建立或扩充紧急备用金","制定月度预算并严格执行","减少非必要支出","评估并优化债务结构"])
    report.warning_signs=["信用卡经常只还最低还款额" if tl>0 else "无信用卡负债","月光族，没有固定储蓄","不知道每月具体花销","没有购买任何保险"]
    return report.to_dict()

def generate_health_report(request):
    report = FinancialHealthReport()
    mi = request.monthly_income; me = request.get_total_monthly_expenses(); ms = mi-me
    ta = request.get_total_assets(); tl = request.get_total_liabilities(); ia = request.assets.get("investments",0)
    if mi>0:
        er = me/mi
        if er<=0.5: report.dimensions["budgeting"]=100
        elif er<=0.7: report.dimensions["budgeting"]=80
        elif er<=0.85: report.dimensions["budgeting"]=60
        elif er<=0.95: report.dimensions["budgeting"]=40
        else: report.dimensions["budgeting"]=20
    else: report.dimensions["budgeting"]=0
    if mi>0:
        sr = ms/mi; report.dimensions["saving"]=min(100,sr*200)
    else: report.dimensions["saving"]=0
    if ta>0:
        ir = ia/ta; report.dimensions["investing"]=min(100,ir*150)
    else: report.dimensions["investing"]=0
    if mi>0:
        md = tl*0.01; dr = md/mi
        if dr<=0.2: report.dimensions["debt"]=100
        elif dr<=0.36: report.dimensions["debt"]=80
        elif dr<=0.5: report.dimensions["debt"]=50
        else: report.dimensions["debt"]=20
    else: report.dimensions["debt"]=50
    ei = request.insurance; ins=0
    if ei.get("life",0)>0: ins+=33
    if ei.get("health",0)>0: ins+=33
    if ei.get("property",0)>0: ins+=34
    report.dimensions["protection"]=ins
    ps=50
    if request.goals: ps+=25
    if request.risk_profile: ps+=25
    report.dimensions["planning"]=ps
    w={"budgeting":0.2,"saving":0.2,"investing":0.15,"debt":0.2,"protection":0.15,"planning":0.1}
    report.overall_score=sum(report.dimensions[k]*w[k] for k in w)
    if report.overall_score>=85: report.score_grade="excellent"
    elif report.overall_score>=70: report.score_grade="good"
    elif report.overall_score>=50: report.score_grade="fair"
    else: report.score_grade="poor"
    report.summary=f"您的家庭财务健康评分{report.overall_score:.0f}分（{report.score_grade}）。月收入{mi:.0f}元，月支出{me:.0f}元，月储蓄{ms:.0f}元，净资产{ta-tl:.0f}元。"
    td=sorted(report.dimensions.items(),key=lambda x:x[1],reverse=True)[:3]
    sm={"budgeting":"预算管理","saving":"储蓄能力","investing":"投资配置","debt":"债务管理","protection":"风险保障","planning":"财务规划"}
    report.top_strengths=[f"{sm[k]}较强（{v:.0f}分）" for k,v in td if v>=70]
    report.top_concerns=[f"{sm[k]}需要改善（{v:.0f}分）" for k,v in td if v<60]
    concerns=[(k,v) for k,v in report.dimensions.items() if v<70]; concerns.sort(key=lambda x:x[1])
    da={"budgeting":("控制不必要支出，建议使用记账App追踪开销","1个月内"),"saving":("提高储蓄率至20%以上，先储后花","3个月内"),"investing":("根据风险偏好配置多元化投资组合","6个月内"),"debt":("制定债务还款计划，优先偿还高息债务","立即"),"protection":("补充必要的保险保障","3个月内"),"planning":("设定明确的财务目标并制定执行计划","1个月内")}
    for i,(dim,score) in enumerate(concerns[:3]):
        a,t=da.get(dim,("改善财务状况","尽快")); report.action_plan.append({"priority":i+1,"action":a,"timeline":t})
    return report.to_dict()

def _exp_rec(sr, expenses):
    recs=[]; total=sum(expenses.values()) if expenses else 0
    if expenses.get("entertainment",0)>total*0.1: recs.append("娱乐支出占比偏高，建议控制在10%以内")
    if expenses.get("food",0)>total*0.3: recs.append("餐饮支出较高，可考虑减少外卖，增加在家做饭")
    if sr<20: recs.append("储蓄率偏低，建议采用'先储后花'策略")
    if not recs: recs.append("支出结构基本合理，继续保持")
    return recs

def _gen_sug(request, sr, dti, efm):
    sug=[]
    if sr<20: sug.append("建议提高储蓄率至20%以上，为未来积累财富")
    if efm<3: sug.append("紧急备用金不足，建议储备3-6个月生活费")
    if dti>50: sug.append("负债率过高，建议优先偿还高息债务")
    if request.assets.get("investments",0)==0: sug.append("建议开始投资，通过多元化配置实现财富增值")
    if request.insurance.get("life",0)==0 and request.insurance.get("health",0)==0: sug.append("建议配置基础保险，转移家庭财务风险")
    if not sug: sug.append("财务状况良好，继续保持当前的理财习惯")
    return sug
