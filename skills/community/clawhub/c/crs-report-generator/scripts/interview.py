from dataclasses import dataclass


QUESTIONS = {
    "year": "您想算哪一年的税？可以说 2024、2025，或者说单子上写的哪年。",
    "residence": "这一年您主要住在哪儿？大部分时间在国内、国内国外两边跑、基本上住在国外，或者说我也不清楚。",
    "residence_followup": "这一年在中国住满半年了吗？家里是不是还在国内？",
    "brokers": "钱放在哪几家了？可以说富途那个、华泰那个，也可以不说，直接把单子传上来。",
    "uploads": "把这一年能找到的月结单、年结单都传上来。能找到多少传多少。",
    "income": "这一年有没有分过红、收过利息，或者外国已经扣过税？不知道就说不知道。",
}

UNCLEAR_RESIDENCE = {"我也不清楚", "不清楚", "不知道", "国内国外两边跑", "基本上住在国外"}


@dataclass
class InterviewState:
    step: str
    question: str | None
    answers: dict


def start_interview() -> InterviewState:
    return InterviewState(step="year", question=QUESTIONS["year"], answers={})


def next_question(state: InterviewState, answer: str) -> InterviewState:
    answers = dict(state.answers)
    if state.step == "year":
        answers["year"] = answer
        return InterviewState(step="residence", question=QUESTIONS["residence"], answers=answers)
    if state.step == "residence":
        answers["residence"] = answer
        if answer.strip() in UNCLEAR_RESIDENCE or "国外" in answer or "不清楚" in answer:
            return InterviewState(
                step="residence_followup",
                question=QUESTIONS["residence_followup"],
                answers=answers,
            )
        return InterviewState(step="brokers", question=QUESTIONS["brokers"], answers=answers)
    if state.step == "residence_followup":
        answers["residence_followup"] = answer
        return InterviewState(step="brokers", question=QUESTIONS["brokers"], answers=answers)
    if state.step == "brokers":
        answers["brokers"] = answer
        return InterviewState(step="uploads", question=QUESTIONS["uploads"], answers=answers)
    if state.step == "uploads":
        answers["uploads"] = answer
        return InterviewState(step="income", question=QUESTIONS["income"], answers=answers)
    answers["income"] = answer
    return InterviewState(step="done", question=None, answers=answers)
