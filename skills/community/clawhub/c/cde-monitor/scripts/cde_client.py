from __future__ import annotations

import json
import math
import re
import time
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from models import AcceptanceReviewResult, PageCapture, QueryRunResult, QueryTarget
from normalizers import dedupe_records, normalize_record


INFO_DISCLOSURE_URL = "https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d"

BREAKTHROUGH_ANNOUNCEMENTS = QueryTarget(
    command="breakthrough-announcements",
    left_tab="突破性治疗公示",
    right_tab="拟突破性治疗品种",
    description="List all drugs currently shown in 拟突破性治疗品种.",
    scope_selector="#breakthroughTherapyTab",
)

BREAKTHROUGH_INCLUDED = QueryTarget(
    command="breakthrough-included-by-company",
    left_tab="突破性治疗公示",
    right_tab="纳入突破性治疗品种名单",
    description="Find company-specific drugs in 纳入突破性治疗品种名单.",
    scope_selector="#breakthroughTherapyTab",
)

BREAKTHROUGH_INCLUDED_BY_DRUG = QueryTarget(
    command="breakthrough-included-by-drug",
    left_tab="突破性治疗公示",
    right_tab="纳入突破性治疗品种名单",
    description="Find drug-specific records in 纳入突破性治疗品种名单.",
    scope_selector="#breakthroughTherapyTab",
)

PRIORITY_ANNOUNCEMENTS = QueryTarget(
    command="priority-announcements",
    left_tab="优先审评公示",
    right_tab="拟优先审评品种公示",
    description="List all drugs currently shown in 拟优先审评品种公示.",
    scope_selector="#priorityReviewTab",
)

PRIORITY_INCLUDED = QueryTarget(
    command="priority-included-by-company",
    left_tab="优先审评公示",
    right_tab="纳入优先审评品种名单",
    description="Find company-specific drugs in 纳入优先审评品种名单.",
    scope_selector="#priorityReviewTab",
)

PRIORITY_INCLUDED_BY_DRUG = QueryTarget(
    command="priority-included-by-drug",
    left_tab="优先审评公示",
    right_tab="纳入优先审评品种名单",
    description="Find drug-specific records in 纳入优先审评品种名单.",
    scope_selector="#priorityReviewTab",
)

IN_REVIEW = QueryTarget(
    command="in-review",
    left_tab="受理品种信息",
    right_tab="在审品种目录浏览",
    description="Query the in-review registration catalog.",
    scope_selector="#content_9f9c74c73e0f8f56a8bfbc646055026d",
)

REVIEW_TASKS = QueryTarget(
    command="review-status-by-acceptance-no",
    left_tab="审评任务公示",
    right_tab="新报任务公示",
    description="Query review task status by acceptance number.",
    scope_selector="#content_369ac7cfeb67c6000c33f85e6f374044",
)


class CDEQueryError(RuntimeError):
    pass


TEXT_FILTER_HINTS = {
    "受理号": (
        "acceptid",
        "acceptid2",
        "acceptid3",
        "acceptid4",
        "acceptidInclude",
        "acceptidPlan",
        "acceptidBreakInclude",
        "acceptidBreakPlan",
    ),
    "药品名称": ("drugname", "drugnameInclude", "drugnamePlan", "drugnameBreakInclude", "drugnameBreakPlan"),
    "企业名称": ("company",),
    "注册申请人": (
        "companyInclude",
        "companyPlan",
        "companyBreakInclude",
        "companyBreakPlan",
        "company",
    ),
}

SELECT_FILTER_HINTS = {
    "年度": ("year",),
    "药品类型": ("drugtype", "drugtypeNewReport"),
    "申请类型": ("applytype", "applytypecdeNewReport", "applytypecdeNewReportZy", "applytypecdeNewReportSw"),
    "公示类型": ("splxtype",),
    "审评任务分类": ("applytypecdeNewReport", "applytypecdeNewReportZy", "applytypecdeNewReportSw"),
}

REVIEW_STAGE_COLUMNS = (
    "药理毒理",
    "临床",
    "药学",
    "统计",
    "临床药理",
    "合规",
)

REVIEW_STAGE_ICON_MAP = {
    "/main/img/lamp_shut.gif": {"code": 1, "label": "本专业已完成审评"},
    "/main/img/lamp_y.jpg": {"code": 2, "label": "本专业排队待审评"},
    "/main/img/lamp.gif": {"code": 3, "label": "本专业正在审评"},
}

MIN_ACCEPTANCE_LOOKUP_YEAR = 2016
MAX_ACCEPTANCE_LOOKUP_YEAR = 2026


class CDEClient:
    def __init__(self, headless: bool = True, timeout: int = 25, max_pages: Optional[int] = None) -> None:
        self.headless = headless
        self.timeout = timeout
        self.max_pages = max_pages

    def query_breakthrough_announcements(self) -> Dict[str, Any]:
        return self._query_target(BREAKTHROUGH_ANNOUNCEMENTS).to_dict()

    def query_breakthrough_included_by_company(self, company: str) -> Dict[str, Any]:
        self._validate_exact_name(company, "company")
        return self._query_target(
            BREAKTHROUGH_INCLUDED,
            text_filters=(("注册申请人", company),),
            applied_filters={"company": company},
        ).to_dict()

    def query_breakthrough_included_by_drug(self, drug: str) -> Dict[str, Any]:
        self._validate_exact_name(drug, "drug")
        return self._query_target(
            BREAKTHROUGH_INCLUDED_BY_DRUG,
            text_filters=(("药品名称", drug),),
            applied_filters={"drug": drug},
        ).to_dict()

    def query_priority_announcements(self) -> Dict[str, Any]:
        return self._query_target(PRIORITY_ANNOUNCEMENTS).to_dict()

    def query_priority_included_by_company(self, company: str) -> Dict[str, Any]:
        self._validate_exact_name(company, "company")
        return self._query_target(
            PRIORITY_INCLUDED,
            text_filters=(("注册申请人", company),),
            applied_filters={"company": company},
        ).to_dict()

    def query_priority_included_by_drug(self, drug: str) -> Dict[str, Any]:
        self._validate_exact_name(drug, "drug")
        return self._query_target(
            PRIORITY_INCLUDED_BY_DRUG,
            text_filters=(("药品名称", drug),),
            applied_filters={"drug": drug},
        ).to_dict()

    def query_in_review_by_company(self, company: str, years: Sequence[int]) -> Dict[str, Any]:
        self._validate_exact_name(company, "company")
        return self._query_in_review(
            text_filter_label="企业名称",
            text_filter_value=company,
            filter_key="company",
            years=years,
        ).to_dict()

    def query_in_review_by_drug(self, drug: str, years: Sequence[int]) -> Dict[str, Any]:
        self._validate_exact_name(drug, "drug")
        return self._query_in_review(
            text_filter_label="药品名称",
            text_filter_value=drug,
            filter_key="drug",
            years=years,
        ).to_dict()

    def query_review_status_by_acceptance_no(self, acceptance_no: str) -> Dict[str, Any]:
        normalized_acceptance_no = self._normalize_acceptance_no(acceptance_no)
        inferred_year = self.infer_acceptance_year(normalized_acceptance_no)
        self._validate_acceptance_lookup_year(inferred_year, normalized_acceptance_no)
        basic_record = self._query_acceptance_basic_info(normalized_acceptance_no)
        if basic_record is None:
            return AcceptanceReviewResult(
                acceptance_no=normalized_acceptance_no,
                inferred_year=inferred_year,
            ).to_dict()

        review_lookup = self._query_review_status_for_basic_info(normalized_acceptance_no, basic_record)
        return AcceptanceReviewResult(
            acceptance_no=normalized_acceptance_no,
            inferred_year=inferred_year,
            basic_info=basic_record.get("normalized"),
            review_status=review_lookup.get("review_status"),
            attempts=review_lookup.get("attempts", []),
            pages_visited=review_lookup.get("pages_visited", 0),
        ).to_dict()

    @staticmethod
    def infer_acceptance_year(acceptance_no: str) -> int:
        normalized = re.sub(r"\s+", "", (acceptance_no or "").upper())
        if not re.fullmatch(r"[A-Z]{4}\d{7,}", normalized):
            raise CDEQueryError(f"Invalid acceptance number: {acceptance_no}")
        return 2000 + int(normalized[4:6])

    def _query_in_review(
        self,
        *,
        text_filter_label: str,
        text_filter_value: str,
        filter_key: str,
        years: Sequence[int],
    ) -> QueryRunResult:
        merged_records: List[Dict[str, Any]] = []
        total_pages = 0
        queried_years: List[int] = []
        for year in years:
            partial = self._query_target(
                IN_REVIEW,
                text_filters=((text_filter_label, text_filter_value),),
                select_filters=(("年度", str(year)),),
                applied_filters={filter_key: text_filter_value, "year": year},
                year=year,
            )
            merged_records.extend(partial.records)
            total_pages += partial.pages_visited
            queried_years.append(year)
        deduped = dedupe_records(merged_records)
        return QueryRunResult(
            command=f"in-review-by-{filter_key}",
            description=IN_REVIEW.description,
            records=deduped,
            applied_filters={filter_key: text_filter_value},
            years_queried=queried_years,
            pages_visited=total_pages,
        )

    def _normalize_acceptance_no(self, acceptance_no: str) -> str:
        normalized = re.sub(r"\s+", "", (acceptance_no or "").upper())
        if not normalized:
            raise CDEQueryError("A non-empty acceptance number is required")
        return normalized

    def _validate_acceptance_lookup_year(self, year: int, acceptance_no: str) -> None:
        if MIN_ACCEPTANCE_LOOKUP_YEAR <= year <= MAX_ACCEPTANCE_LOOKUP_YEAR:
            return
        raise CDEQueryError(
            "该受理号推断年份超出当前 CDE 页面可查询范围: "
            f"{acceptance_no} -> {year}，当前支持年份为 {MIN_ACCEPTANCE_LOOKUP_YEAR} 到 {MAX_ACCEPTANCE_LOOKUP_YEAR}"
        )

    def _query_acceptance_basic_info(self, acceptance_no: str) -> Optional[Dict[str, Any]]:
        inferred_year = self.infer_acceptance_year(acceptance_no)
        result = self._query_target(
            IN_REVIEW,
            text_filters=(("受理号", acceptance_no),),
            select_filters=(("年度", str(inferred_year)),),
            applied_filters={"acceptance_no": acceptance_no, "year": inferred_year},
            year=inferred_year,
        )
        for record in result.records:
            normalized = record.get("normalized", {})
            if self._normalize_acceptance_no(normalized.get("acceptance_no", "")) == acceptance_no:
                return record
        return None

    def _query_review_status_for_basic_info(
        self,
        acceptance_no: str,
        basic_record: Dict[str, Any],
    ) -> Dict[str, Any]:
        plans = self._build_review_search_plans(basic_record)
        attempts: List[Dict[str, Any]] = []
        pages_visited = 0
        driver = self._build_driver()
        try:
            self._open_listing_page(driver)
            self._clear_logs(driver)
            self._click_left_tab(driver, REVIEW_TASKS.left_tab)
            self._clear_logs(driver)
            self._click_right_tab(driver, REVIEW_TASKS.right_tab, scope_selector=REVIEW_TASKS.scope_selector)
            for plan in plans:
                filtered_attempt = self._run_review_status_attempt(
                    driver,
                    acceptance_no,
                    plan,
                    use_acceptance_filter=True,
                )
                attempts.append(filtered_attempt["attempt"])
                pages_visited += filtered_attempt["attempt"].get("pages_scanned", 0)
                if filtered_attempt.get("review_status") is not None:
                    return {
                        "review_status": filtered_attempt["review_status"],
                        "attempts": attempts,
                        "pages_visited": pages_visited,
                    }

                if not filtered_attempt["attempt"].get("warning"):
                    continue

                broadened_attempt = self._run_review_status_attempt(
                    driver,
                    acceptance_no,
                    plan,
                    use_acceptance_filter=False,
                )
                attempts.append(broadened_attempt["attempt"])
                pages_visited += broadened_attempt["attempt"].get("pages_scanned", 0)
                if broadened_attempt.get("review_status") is not None:
                    return {
                        "review_status": broadened_attempt["review_status"],
                        "attempts": attempts,
                        "pages_visited": pages_visited,
                    }

            return {"review_status": None, "attempts": attempts, "pages_visited": pages_visited}
        finally:
            driver.quit()

    def _build_review_search_plans(self, basic_record: Dict[str, Any]) -> List[Dict[str, Any]]:
        normalized = basic_record.get("normalized", {})
        drug_type = normalized.get("drug_type") or ""
        application_type = normalized.get("application_type") or ""
        acceptance_no = normalized.get("acceptance_no") or ""

        public_type = self._map_public_notice_type(drug_type, acceptance_no)
        task_category = self._map_review_task_category(public_type, application_type, acceptance_no)
        biologics_subtypes = self._map_biologics_subtypes(public_type, drug_type)

        plans: List[Dict[str, Any]] = []
        for biologics_subtype in biologics_subtypes:
            plans.append(
                {
                    "public_type": public_type,
                    "task_category": task_category,
                    "biologics_subtype": biologics_subtype,
                }
            )
        return plans

    def _map_public_notice_type(self, drug_type: str, acceptance_no: str) -> str:
        if "中药" in drug_type:
            return "中药审评序列公示"
        if "生物" in drug_type or "预防用" in drug_type or "治疗用" in drug_type:
            return "生物制品审评序列公示"

        normalized = self._normalize_acceptance_no(acceptance_no)
        third_letter = normalized[2]
        if third_letter == "Z":
            return "中药审评序列公示"
        if third_letter == "S":
            return "生物制品审评序列公示"
        return "化药审评序列公示"

    def _map_biologics_subtypes(self, public_type: str, drug_type: str) -> List[Optional[str]]:
        if public_type != "生物制品审评序列公示":
            return [None]
        if "治疗用" in drug_type:
            return ["治疗用生物制品"]
        if "预防用" in drug_type:
            return ["预防用生物制品"]
        return ["治疗用生物制品", "预防用生物制品"]

    def _map_review_task_category(self, public_type: str, application_type: str, acceptance_no: str) -> str:
        normalized = self._normalize_acceptance_no(acceptance_no)
        second_letter = normalized[1]
        fourth_letter = normalized[3]

        if public_type == "生物制品审评序列公示":
            if "补充" in application_type or second_letter == "B" or fourth_letter == "B":
                return "补充申请"
            if "再注册" in application_type or fourth_letter == "Z":
                return "再注册"
            if "临床" in application_type or fourth_letter == "L":
                return "临床试验申请"
            return "上市申请"

        if "补充" in application_type or second_letter == "B" or fourth_letter == "B":
            return "补充申请"
        if "进口再注册" in application_type:
            return "进口再注册"
        if "复审" in application_type or fourth_letter == "R":
            return "复审"
        if "验证性临床" in application_type:
            return "验证性临床"
        if "仿制" in application_type or second_letter == "Y":
            return "ANDA"
        if "临床" in application_type or fourth_letter == "L":
            return "IND"
        return "NDA"

    def _run_review_status_attempt(
        self,
        driver: webdriver.Chrome,
        acceptance_no: str,
        plan: Dict[str, Any],
        *,
        use_acceptance_filter: bool,
    ) -> Dict[str, Any]:
        scope_selector = REVIEW_TASKS.scope_selector
        self._apply_review_status_filters(
            driver,
            acceptance_no,
            plan,
            use_acceptance_filter=use_acceptance_filter,
            scope_selector=scope_selector,
        )
        self._submit_review_task_search(driver, scope_selector=scope_selector)
        time.sleep(1.5)

        page_payload = self._scrape_review_task_page(driver, scope_selector=scope_selector)
        pages_scanned = 1
        review_status = self._find_review_task_row(page_payload["rows"], acceptance_no)

        if review_status is None and not page_payload["warning"]:
            total_pages = page_payload.get("total_pages", 1)
            for page in range(2, total_pages + 1):
                if not self._go_to_page(driver, page, scope_selector=scope_selector):
                    break
                time.sleep(1.0)
                page_payload = self._scrape_review_task_page(driver, scope_selector=scope_selector)
                pages_scanned += 1
                review_status = self._find_review_task_row(page_payload["rows"], acceptance_no)
                if review_status is not None:
                    break

        attempt = {
            "public_type": plan["public_type"],
            "task_category": plan["task_category"],
            "biologics_subtype": plan.get("biologics_subtype"),
            "used_acceptance_filter": use_acceptance_filter,
            "warning": page_payload.get("warning"),
            "pages_scanned": pages_scanned,
            "found": review_status is not None,
        }
        return {"attempt": attempt, "review_status": review_status}

    def _apply_review_status_filters(
        self,
        driver: webdriver.Chrome,
        acceptance_no: str,
        plan: Dict[str, Any],
        *,
        use_acceptance_filter: bool,
        scope_selector: str,
    ) -> None:
        self._select_filter(driver, "公示类型", plan["public_type"], scope_selector=scope_selector)
        if plan.get("biologics_subtype"):
            self._select_filter(driver, "药品类型", plan["biologics_subtype"], scope_selector=scope_selector)
        self._select_filter(driver, "审评任务分类", plan["task_category"], scope_selector=scope_selector)
        self._fill_text_filter(
            driver,
            "受理号",
            acceptance_no if use_acceptance_filter else "",
            scope_selector=scope_selector,
        )

    def _submit_review_task_search(self, driver: webdriver.Chrome, *, scope_selector: str) -> None:
        script = """
        const scopeSelector = arguments[0];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
                const button = Array.from(scope.querySelectorAll('button.searchBtn')).find((candidate) =>
                    (candidate.getAttribute('onclick') || '').includes("getNewReportList('xb')")
                );
        if (!button) {
          return false;
        }
        button.click();
        return true;
        """
        if not driver.execute_script(script, scope_selector):
            raise CDEQueryError("Could not find the new-review search button on the CDE page")

    def _scrape_review_task_page(self, driver: webdriver.Chrome, *, scope_selector: str) -> Dict[str, Any]:
        script = """
        const scopeRoot = document.querySelector(arguments[0]);
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
        const warnNode = scope.querySelector('#hightLightWarn_xb');
        const countNode = scope.querySelector('#newReportPage .layui-laypage-count');
        const currentNode = scope.querySelector('#newReportPage .layui-laypage-curr em:last-child');
        const limitNode = scope.querySelector('#newReportPage .layui-laypage-limits option:checked');
        const countMatch = countNode && countNode.textContent ? countNode.textContent.match(/共\s*(\d+)\s*条/) : null;
        const totalRecords = countMatch ? parseInt(countMatch[1], 10) : 0;
        const pageSize = limitNode ? parseInt(limitNode.value || limitNode.textContent, 10) : 10;
        const totalPages = totalRecords && pageSize ? Math.max(1, Math.ceil(totalRecords / pageSize)) : 1;
        const currentPage = currentNode ? parseInt(currentNode.textContent, 10) : 1;
        const rows = Array.from(scope.querySelectorAll('#newReportTbody tr')).map((row) => {
          const cells = Array.from(row.querySelectorAll('td'));
          const stageCells = cells.slice(5, 11).map((cell) => {
            const img = cell.querySelector('img');
            return img ? img.getAttribute('src') || '' : '';
          });
          const acceptanceCell = cells[1] || null;
          return {
            sequence: (cells[0]?.innerText || '').trim(),
            acceptance_no: (acceptanceCell?.innerText || '').trim(),
            drug_name: (cells[2]?.innerText || '').trim(),
            entered_center_at: (cells[3]?.innerText || '').trim(),
            review_state: (cells[4]?.innerText || '').trim(),
            remark: (cells[11]?.innerText || '').trim(),
            stage_icons: stageCells,
            is_highlighted: Boolean(acceptanceCell && acceptanceCell.querySelector('font')),
          };
        }).filter((row) => row.acceptance_no);
        return {
          warning: warnNode ? (warnNode.innerText || '').trim() : '',
          current_page: currentPage,
          total_pages: totalPages,
          total_records: totalRecords,
          rows,
        };
        """
        page_payload = driver.execute_script(script, scope_selector)
        rows = [self._normalize_review_task_row(row) for row in page_payload.get("rows", [])]
        return {
            "warning": page_payload.get("warning") or "",
            "current_page": page_payload.get("current_page", 1),
            "total_pages": page_payload.get("total_pages", 1),
            "total_records": page_payload.get("total_records", 0),
            "rows": rows,
        }

    def _normalize_review_task_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        stages: Dict[str, Dict[str, Any]] = {}
        for column, icon in zip(REVIEW_STAGE_COLUMNS, row.get("stage_icons", [])):
            stage_info = REVIEW_STAGE_ICON_MAP.get(icon, {"code": 0, "label": "本专业未启动"})
            stages[column] = {
                "code": stage_info["code"],
                "label": stage_info["label"],
                "icon": icon,
            }
        return {
            "sequence": row.get("sequence"),
            "acceptance_no": row.get("acceptance_no"),
            "drug_name": row.get("drug_name"),
            "entered_center_at": row.get("entered_center_at"),
            "review_state": row.get("review_state"),
            "remark": row.get("remark"),
            "is_highlighted": bool(row.get("is_highlighted")),
            "stages": stages,
        }

    def _find_review_task_row(self, rows: Sequence[Dict[str, Any]], acceptance_no: str) -> Optional[Dict[str, Any]]:
        for row in rows:
            if self._normalize_acceptance_no(row.get("acceptance_no", "")) == acceptance_no:
                return row
        return None

    def _query_target(
        self,
        target: QueryTarget,
        *,
        text_filters: Iterable[Tuple[str, str]] = (),
        select_filters: Iterable[Tuple[str, str]] = (),
        applied_filters: Optional[Dict[str, Any]] = None,
        year: Optional[int] = None,
    ) -> QueryRunResult:
        driver = self._build_driver()
        try:
            self._open_listing_page(driver)
            self._clear_logs(driver)
            self._click_left_tab(driver, target.left_tab)
            if target.right_tab:
                self._clear_logs(driver)
                self._click_right_tab(driver, target.right_tab, scope_selector=target.scope_selector)

            if text_filters or select_filters:
                self._clear_logs(driver)
                for label, value in select_filters:
                    self._select_filter(driver, label, value, scope_selector=target.scope_selector)
                for label, value in text_filters:
                    self._fill_text_filter(driver, label, value, scope_selector=target.scope_selector)
                self._submit_search(driver, scope_selector=target.scope_selector)

            first_page = self._wait_for_payload(driver, page=1)
            total_pages = self._detect_total_pages(driver, first_page, scope_selector=target.scope_selector)
            if self.max_pages is not None:
                total_pages = min(total_pages, max(1, self.max_pages))

            records = [
                normalize_record(
                    raw_record,
                    source_menu=target.left_tab,
                    source_tab=target.right_tab or target.left_tab,
                    page=1,
                    year=year,
                )
                for raw_record in first_page.records
            ]
            pages_visited = 1
            seen_page_keys = {self._page_key(first_page.records)}

            for page in range(2, total_pages + 1):
                self._clear_logs(driver)
                if not self._go_to_page(driver, page, scope_selector=target.scope_selector):
                    break
                capture = self._wait_for_payload(driver, page=page)
                page_key = self._page_key(capture.records)
                if not capture.records or page_key in seen_page_keys:
                    break
                seen_page_keys.add(page_key)
                pages_visited += 1
                records.extend(
                    normalize_record(
                        raw_record,
                        source_menu=target.left_tab,
                        source_tab=target.right_tab or target.left_tab,
                        page=page,
                        year=year,
                    )
                    for raw_record in capture.records
                )

            return QueryRunResult(
                command=target.command,
                description=target.description,
                records=dedupe_records(records),
                applied_filters=applied_filters or {},
                years_queried=[year] if year is not None else [],
                pages_visited=pages_visited,
            )
        finally:
            driver.quit()

    def _build_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1200")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--lang=zh-CN")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        )
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException as exc:
            raise CDEQueryError(
                "Could not start Chrome via Selenium. Check Chrome installation and local driver support."
            ) from exc
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4]});
                """
            },
        )
        return driver

    def _open_listing_page(self, driver: webdriver.Chrome) -> None:
        driver.get(INFO_DISCLOSURE_URL)
        WebDriverWait(driver, self.timeout).until(
            lambda current_driver: current_driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1.5)

    def _click_left_tab(self, driver: webdriver.Chrome, text: str) -> None:
        script = """
        const targetText = arguments[0];
        const normalize = (value) => (value || '').replace(/\s+/g, '').replace(/[：:]/g, '').trim();
        const target = normalize(targetText);
        const items = Array.from(document.querySelectorAll('.etcd_nav_ul li'));
        for (const item of items) {
            if (normalize(item.textContent || '') !== target) continue;
            item.click();
            return true;
        }
        return false;
        """
        if not driver.execute_script(script, text) and not self._click_element_by_exact_text(driver, text, exclude_left=False):
            raise CDEQueryError(f"Could not find left navigation tab: {text}")
        time.sleep(1.5)

    def _click_right_tab(self, driver: webdriver.Chrome, text: str, *, scope_selector: Optional[str] = None) -> None:
        if not self._click_element_by_exact_text(driver, text, exclude_left=True, scope_selector=scope_selector):
            raise CDEQueryError(f"Could not find right-side tab: {text}")
        time.sleep(1.5)

    def _click_element_by_exact_text(
        self,
        driver: webdriver.Chrome,
        text: str,
        *,
        exclude_left: bool,
        scope_selector: Optional[str] = None,
    ) -> bool:
        script = """
        const targetText = arguments[0];
        const excludeLeft = arguments[1];
        const scopeSelector = arguments[2];
        const scope = scopeSelector ? document.querySelector(scopeSelector) : document;
        const elements = (scope || document).querySelectorAll('a, span, button, li, div');
        const leftSelectors = '.left-nav, .sidebar, .menu-list, .el-menu, [class*="left"]';
        const normalize = (value) => (value || '').replace(/\s+/g, '').replace(/[：:]/g, '').trim();
        const isVisible = (element) => {
            const style = window.getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
        };
        const normalizedTarget = normalize(targetText);
        let containsMatch = null;
        for (const element of elements) {
            if (!isVisible(element)) continue;
            const content = normalize(element.textContent || '');
            if (!content) continue;
            if (excludeLeft && element.closest(leftSelectors)) continue;
            if (content === normalizedTarget) {
                element.click();
                return true;
            }
            if (content.includes(normalizedTarget) || normalizedTarget.includes(content)) {
                if (!containsMatch || content.length < containsMatch.content.length) {
                    containsMatch = { element, content };
                }
            }
        }
        if (containsMatch) {
            containsMatch.element.click();
            return true;
        }
        return false;
        """
        return bool(driver.execute_script(script, text, exclude_left, scope_selector))

    def _fill_text_filter(
        self,
        driver: webdriver.Chrome,
        label: str,
        value: str,
        *,
        scope_selector: Optional[str] = None,
    ) -> None:
        script = """
        const labelText = arguments[0];
        const targetValue = arguments[1];
        const scopeSelector = arguments[2];
                const preferredIds = arguments[3] || [];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
                const setValue = (input, currentValue) => {
                    const descriptor = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
                    if (descriptor && descriptor.set) {
                        descriptor.set.call(input, currentValue);
                    } else {
                        input.value = currentValue;
                    }
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                };
                for (const preferredId of preferredIds) {
                    const escapedId = window.CSS && CSS.escape ? CSS.escape(preferredId) : preferredId;
                    const direct = scope.querySelector(`#${escapedId}`) || scope.querySelector(`input[name="${preferredId}"], textarea[name="${preferredId}"]`);
                    if (direct) {
                        setValue(direct, targetValue);
                        return true;
                    }
                }
        const candidates = scope.querySelectorAll('label, span, div, td, th');
        const matchLabel = (text) => text && text.replace(/[:：]/g, '').trim().includes(labelText);
        for (const candidate of candidates) {
          const text = (candidate.textContent || '').trim();
          if (!text || text.length > 40) continue;
          if (!matchLabel(text)) continue;
          let node = candidate;
          for (let depth = 0; depth < 4 && node; depth += 1) {
            const input = node.querySelector('input, textarea');
            if (input) {
              setValue(input, targetValue);
              return true;
            }
            node = node.parentElement;
          }
        }
        return false;
        """
        preferred_ids = list(TEXT_FILTER_HINTS.get(label, ()))
        if not driver.execute_script(script, label, value, scope_selector, preferred_ids):
            raise CDEQueryError(f"Could not find text filter labeled {label}")
        time.sleep(0.4)

    def _select_filter(
        self,
        driver: webdriver.Chrome,
        label: str,
        value: str,
        *,
        scope_selector: Optional[str] = None,
    ) -> None:
        script = """
        const labelText = arguments[0];
        const targetValue = arguments[1];
        const scopeSelector = arguments[2];
            const preferredIds = arguments[3] || [];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
                const setSelectValue = (select) => {
                    for (const option of select.options) {
                        const optionText = (option.textContent || '').trim();
                        if (optionText === targetValue || option.value === targetValue) {
                            select.value = option.value;
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                    }
                    return false;
                };
                let preferredMatch = false;
                for (const preferredId of preferredIds) {
                    const escapedId = window.CSS && CSS.escape ? CSS.escape(preferredId) : preferredId;
                    const direct = scope.querySelector(`#${escapedId}`) || scope.querySelector(`select[name="${preferredId}"]`);
                    if (direct && setSelectValue(direct)) {
                        preferredMatch = true;
                    }
                }
                if (preferredMatch) {
                    return true;
                }
        const candidates = scope.querySelectorAll('label, span, div, td, th');
        const matchLabel = (text) => text && text.replace(/[:：]/g, '').trim().includes(labelText);
        for (const candidate of candidates) {
            const text = (candidate.textContent || '').trim();
            if (!text || text.length > 40) continue;
            if (!matchLabel(text)) continue;
            let node = candidate;
            for (let depth = 0; depth < 4 && node; depth += 1) {
                const select = node.querySelector('select');
                if (select && setSelectValue(select)) {
                    return true;
                }
                node = node.parentElement;
            }
        }
        return false;
        """
        preferred_ids = list(SELECT_FILTER_HINTS.get(label, ()))
        if not driver.execute_script(script, label, value, scope_selector, preferred_ids):
            raise CDEQueryError(f"Could not find select filter labeled {label}")
        time.sleep(0.4)

    def _submit_search(self, driver: webdriver.Chrome, *, scope_selector: Optional[str] = None) -> None:
        script = """
        const scopeSelector = arguments[0];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
                const candidates = Array.from(scope.querySelectorAll('button, a, span, div'));
        const labels = ['查询', '查找', '搜索'];
                const score = (candidate) => {
                    let current = 0;
                    if (candidate.tagName === 'BUTTON') current += 100;
                    if (candidate.tagName === 'A') current += 80;
                    if (candidate.getAttribute('onclick')) current += 40;
                    if ((candidate.className || '').includes('searchBtn')) current += 20;
                    return current;
                };
                candidates.sort((left, right) => score(right) - score(left));
                for (const candidate of candidates) {
          const text = (candidate.textContent || '').trim();
          if (!labels.includes(text)) continue;
          if (candidate.closest('.layui-laypage')) continue;
          candidate.click();
          return true;
        }
        return false;
        """
        if not driver.execute_script(script, scope_selector):
            raise CDEQueryError("Could not find the search button on the CDE page")
        time.sleep(1.5)

    def _wait_for_payload(self, driver: webdriver.Chrome, *, page: int) -> PageCapture:
        deadline = time.time() + self.timeout
        best_capture: Optional[PageCapture] = None
        best_size = -1
        while time.time() < deadline:
            logs = driver.get_log("performance")
            for entry in logs:
                capture = self._extract_capture_from_log(driver, entry, page)
                if capture is None:
                    continue
                size = len(capture.records)
                if size > best_size:
                    best_capture = capture
                    best_size = size
            if best_capture is not None:
                return best_capture
            time.sleep(0.3)
        raise CDEQueryError("Timed out while waiting for a CDE data response")

    def _extract_capture_from_log(
        self,
        driver: webdriver.Chrome,
        entry: Dict[str, Any],
        page: int,
    ) -> Optional[PageCapture]:
        try:
            message = json.loads(entry["message"]).get("message", {})
        except (KeyError, TypeError, json.JSONDecodeError):
            return None
        if message.get("method") != "Network.responseReceived":
            return None
        params = message.get("params", {})
        response = params.get("response", {})
        request_id = params.get("requestId")
        url = response.get("url", "")
        mime_type = response.get("mimeType", "")
        if not request_id or "cde.org.cn" not in url:
            return None
        if "json" not in mime_type.lower() and "api" not in url.lower() and "list" not in url.lower():
            return None
        try:
            body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        except WebDriverException:
            return None
        raw_body = body.get("body", "")
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return None
        capture = PageCapture(page=page, request_url=url, payload=payload)
        if self._is_result_payload(payload):
            return capture
        return None

    def _is_result_payload(self, payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False
        data = payload.get("data")
        if isinstance(data, dict):
            records = data.get("records")
            if isinstance(records, list):
                return True
            for key in ("pages", "totalPage", "pageCount", "total", "size"):
                if key in data:
                    return True
        records = payload.get("records")
        return isinstance(records, list)

    def _detect_total_pages(
        self,
        driver: webdriver.Chrome,
        first_page: PageCapture,
        *,
        scope_selector: Optional[str] = None,
    ) -> int:
        payload = first_page.payload.get("data") if isinstance(first_page.payload, dict) else None
        if isinstance(payload, dict):
            for key in ("pages", "totalPage", "pageCount"):
                value = payload.get(key)
                if isinstance(value, int) and value > 0:
                    return value
            total = payload.get("total")
            if isinstance(total, int) and total > 0 and first_page.records:
                page_size = payload.get("size") or len(first_page.records)
                if isinstance(page_size, int) and page_size > 0:
                    return max(1, math.ceil(total / page_size))

        script = """
        const scopeSelector = arguments[0];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
        const countNode = scope.querySelector('.layui-laypage-count');
        if (countNode) {
          const match = countNode.textContent.match(/共\s*(\d+)\s*条/);
          if (match) {
            const limits = Array.from(scope.querySelectorAll('.layui-laypage-limits option')).map((option) => ({
              selected: option.selected,
              value: parseInt(option.value || option.textContent, 10),
            }));
            const selectedLimit = limits.find((item) => !Number.isNaN(item.value) && item.selected);
            return { total: parseInt(match[1], 10), pageSize: selectedLimit ? selectedLimit.value : 10 };
          }
        }
        const buttons = scope.querySelectorAll('.layui-laypage a');
        let maxPage = 1;
        for (const button of buttons) {
          const value = parseInt((button.textContent || '').trim(), 10);
          if (!Number.isNaN(value) && value > maxPage) {
            maxPage = value;
          }
        }
        return { maxPage };
        """
        info = driver.execute_script(script, scope_selector)
        if isinstance(info, dict):
            total = info.get("total")
            page_size = info.get("pageSize") or 10
            if isinstance(total, int) and total > 0:
                return max(1, math.ceil(total / page_size))
            max_page = info.get("maxPage")
            if isinstance(max_page, int) and max_page > 0:
                return max_page
        return 1

    def _go_to_page(self, driver: webdriver.Chrome, page: int, *, scope_selector: Optional[str] = None) -> bool:
        script = """
        const pageNumber = String(arguments[0]);
        const scopeSelector = arguments[1];
        const scopeRoot = scopeSelector ? document.querySelector(scopeSelector) : document;
        const scope = scopeRoot && scopeRoot.querySelector('.layui-tab-content .layui-show')
          ? scopeRoot.querySelector('.layui-tab-content .layui-show')
          : (scopeRoot || document);
        let input = null;
        const skipDiv = scope.querySelector('.layui-laypage-skip');
        if (skipDiv) {
          input = skipDiv.querySelector('input.layui-input');
        }
        if (!input) {
          const inputs = scope.querySelectorAll('input.layui-input');
          for (const candidate of inputs) {
            const parentText = candidate.parentElement ? candidate.parentElement.textContent : '';
            if (parentText && parentText.includes('到第') && parentText.includes('页')) {
              input = candidate;
              break;
            }
          }
        }
        if (!input) {
          return false;
        }
        const descriptor = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
        if (descriptor && descriptor.set) {
          descriptor.set.call(input, pageNumber);
        } else {
          input.value = pageNumber;
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        const button = scope.querySelector('.layui-laypage-btn');
        if (!button) {
          return false;
        }
        button.click();
        return true;
        """
        success = bool(driver.execute_script(script, page, scope_selector))
        if success:
            time.sleep(1.5)
        return success

    def _clear_logs(self, driver: webdriver.Chrome) -> None:
        try:
            driver.get_log("performance")
        except WebDriverException:
            return

    def _page_key(self, records: List[Dict[str, Any]]) -> str:
        return json.dumps(records, ensure_ascii=False, sort_keys=True)

    def _validate_exact_name(self, value: str, label: str) -> None:
        if not value or not value.strip():
            raise CDEQueryError(f"A non-empty {label} name is required")
