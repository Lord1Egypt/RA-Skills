#!/usr/bin/env python3
"""
企业征信核查测试用例
"""

def test_low_risk_enterprise():
    """测试低风险企业"""
    check_results = {
        "pbc_credit": {"rating": "正常", "overdue": 0},
        "business_status": {"status": "存续", "abnormal": False},
        "execution": {"dishonest": False, "execution": False},
        "penalty": {"has_penalty": False},
        "litigation": {"total_cases": 1, "ip_disputes": 0}
    }
    
    from risk_calculator import calculate_risk_score
    result = calculate_risk_score(check_results)
    
    assert result["total_score"] >= 90, f"低风险企业评分应≥90，实际{result['total_score']}"
    assert result["risk_level"] == "low", f"低风险企业应为low，实际{result['risk_level']}"
    print("✅ 低风险企业测试通过")

def test_medium_risk_enterprise():
    """测试中等风险企业"""
    check_results = {
        "pbc_credit": {"rating": "关注", "overdue": 0},
        "business_status": {"status": "存续", "abnormal": True, "abnormal_removed": True},
        "execution": {"dishonest": False, "execution": True, "execution_amount": 10},
        "penalty": {"has_penalty": True, "amount": 5},
        "litigation": {"total_cases": 3, "ip_disputes": 0}
    }
    
    from risk_calculator import calculate_risk_score
    result = calculate_risk_score(check_results)
    
    assert 60 <= result["total_score"] < 80, f"中等风险企业评分应60-79，实际{result['total_score']}"
    assert result["risk_level"] in ["low", "medium"], f"应为low或medium"
    print("✅ 中等风险企业测试通过")

def test_high_risk_enterprise():
    """测试高风险企业"""
    check_results = {
        "pbc_credit": {"rating": "次级", "overdue": 0},
        "business_status": {"status": "存续", "abnormal": False},
        "execution": {"dishonest": False, "execution": False},
        "penalty": {"has_penalty": False},
        "litigation": {"total_cases": 0, "ip_disputes": 0}
    }
    
    from risk_calculator import calculate_risk_score
    result = calculate_risk_score(check_results)
    
    assert result["total_score"] < 40, f"高风险企业评分应<40，实际{result['total_score']}"
    assert result["risk_level"] == "critical", f"应为critical"
    print("✅ 高风险企业测试通过")

def test_hard_stop_dishonest():
    """测试硬终止-失信被执行人"""
    check_results = {
        "pbc_credit": {"rating": "正常", "overdue": 0},
        "business_status": {"status": "存续", "abnormal": False},
        "execution": {"dishonest": True, "dishonest_records": [{"amount": 100}]},
        "penalty": {"has_penalty": False},
        "litigation": {"total_cases": 0, "ip_disputes": 0}
    }
    
    from risk_calculator import calculate_risk_score
    result = calculate_risk_score(check_results)
    
    assert result["risk_level"] == "critical", "失信被执行人应为critical"
    print("✅ 硬终止-失信被执行人测试通过")

def test_weight_calculation():
    """测试权重计算"""
    from risk_calculator import calculate_risk_score
    
    check_results = {
        "pbc_credit": {"rating": "正常", "overdue": 0},
        "business_status": {"status": "存续", "abnormal": False},
        "execution": {"dishonest": False, "execution": False},
        "penalty": {"has_penalty": False},
        "litigation": {"total_cases": 0, "ip_disputes": 0}
    }
    
    result = calculate_risk_score(check_results)
    
    # 验证权重
    assert "component_scores" in result
    assert "weights" in result
    assert result["weights"]["pbc_credit"] == 0.40
    assert result["weights"]["business_status"] == 0.25
    assert result["weights"]["execution"] == 0.20
    assert result["weights"]["penalty"] == 0.10
    assert result["weights"]["litigation"] == 0.05
    
    print("✅ 权重计算测试通过")

if __name__ == "__main__":
    test_low_risk_enterprise()
    test_medium_risk_enterprise()
    test_high_risk_enterprise()
    test_hard_stop_dishonest()
    test_weight_calculation()
    print("\n所有测试通过！🎉")
