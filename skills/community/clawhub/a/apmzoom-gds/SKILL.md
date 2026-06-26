---
name: APM 상품 관리 API
description: "APM 플랫폼의 상품 관리 API 모음. 관리자용 상품 추가/삭제/수정/가격·재고·할인 관리 17개 + 사용자용 상품 조회/검색/카테고리/추천/유사 상품/이미지 검색 16개, 총 33개 엔드포인트. 모든 엔드포인트는 먼저 ids_*_login으로 access_token 획득 후 authcode 헤더(HH + token)로 호출. last_update_time 커서 페이지네이션 사용. 중국어/한국어 키워드 검색 지원."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - APM_USER_TOKEN
    primaryEnv: APM_USER_TOKEN
    homepage: https://github.com/apmzoom-ai/apm-skills
---

# APM 상품 관리 API

APM 플랫폼의 상품 관리 API 모음. 관리자용 상품 추가/삭제/수정/가격·재고·할인 관리 17개 + 사용자용 상품 조회/검색/카테고리/추천/유사 상품/이미지 검색 16개, 총 33개 엔드포인트. 모든 엔드포인트는 먼저 ids_*_login으로 access_token 획득 후 authcode 헤더(HH + token)로 호출. last_update_time 커서 페이지네이션 사용. 중국어/한국어 키워드 검색 지원.

## 공통 규약

- **Base URL**: `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com`
- **요청 헤더**: `v=7.0.1`, `p=1`, `t=<unix초>`, `lang=zh-cn`
- **인증 헤더**: `authcode: "HH " + access_token` (로그인 계열 제외)
- **서명**: `sign = MD5(<params> + <salt>).toUpperCase()` — 엔드포인트별 salt는 각 문서 참조
- **성공 코드**: `code=100`, 결과는 `result` 필드
- **페이지네이션**: `last_update_time` 커서 방식, `page_size=20`

## 엔드포인트 목록 (33개)

- [`gds_m_addgoods`](gds_m_addgoods.md) — **상품 정보 추가[판매자]** · `POST /gds/app/m_addgoods`
- [`gds_m_delgoods`](gds_m_delgoods.md) — **상품 정보 삭제[판매자]** · `GET /gds/app/m_delgoods`
- [`gds_m_editgoods`](gds_m_editgoods.md) — **상품 정보 수정[판매자]** · `POST /gds/app/m_editgoods`
- [`gds_m_editgoodsdiscount`](gds_m_editgoodsdiscount.md) — **상품 할인 수정[판매자]** · `POST /gds/app/m_editgoodsdiscount`
- [`gds_m_editgoodsdiscountprice`](gds_m_editgoodsdiscountprice.md) — **상품 할인 가격 수정[판매자]** · `POST /gds/app/m_editgoodsdiscountprice`
- [`gds_m_editgoodsprice`](gds_m_editgoodsprice.md) — **상품 가격 수정[판매자]** · `POST /gds/app/m_editgoodsprice`
- [`gds_m_editgoodssell`](gds_m_editgoodssell.md) — **상품 진열 상태 수정[판매자]** · `POST /gds/app/m_editgoodssell`
- [`gds_m_editgoodsskuprice`](gds_m_editgoodsskuprice.md) — **상품 규격 재고 가격 수정[판매자]** · `POST /gds/app/m_editgoodsskuprice`
- [`gds_m_editgoodsstock`](gds_m_editgoodsstock.md) — **상품 재고 수정[판매자]** · `POST /gds/app/m_editgoodsstock`
- [`gds_m_goodsclassattributealllist`](gds_m_goodsclassattributealllist.md) — **상품 카테고리 속성 목록 조회[판매자]** · `GET /gds/app/m_goodsclassattributealllist`
- [`gds_m_goodsclasslist`](gds_m_goodsclasslist.md) — **상품 카테고리 목록 조회[판매자]** · `GET /gds/app/m_goodsclasslist`
- [`gds_m_goodsclassspecalllist`](gds_m_goodsclassspecalllist.md) — **상품 카테고리 규격 목록 조회[판매자]** · `GET /gds/app/m_goodsclassspecalllist`
- [`gds_m_goodseditinfo`](gds_m_goodseditinfo.md) — **상품 편집 상세 정보 조회[판매자]** · `GET /gds/app/m_goodseditinfo`
- [`gds_m_goodseditskuinfo`](gds_m_goodseditskuinfo.md) — **상품 규격 정보 조회[판매자]** · `GET /gds/app/m_goodseditskuinfo`
- [`gds_m_goodsmakeaddresslist`](gds_m_goodsmakeaddresslist.md) — **원산지 목록 조회[판매자]** · `GET /gds/app/m_goodsmakeaddresslist`
- [`gds_m_goodsskuiscandel`](gds_m_goodsskuiscandel.md) — **상품 SKU 삭제 가능 여부 조회[판매자]** · `GET /gds/app/m_goodsskuiscandel`
- [`gds_m_storegoodslist`](gds_m_storegoodslist.md) — **판매자 상품 목록 조회** · `GET /gds/app/m_storegoodslist`
- [`gds_u_addgoods`](gds_u_addgoods.md) — **상품 정보 추가[셀프 추가 결제]** · `POST /gds/app/u_addgoods`
- [`gds_u_categorygoodslist`](gds_u_categorygoodslist.md) — **상품 카테고리별 상품 목록 조회[사용자]** · `GET /gds/app/u_categorygoodslist`
- [`gds_u_complaintgoodsprice`](gds_u_complaintgoodsprice.md) — **상품 가격 신고[사용자]** · `POST /gds/app/u_complaintgoodsprice`
- [`gds_u_dategoodslist`](gds_u_dategoodslist.md) — **일자별 신상품 목록 조회[사용자]** · `GET /gds/app/u_dategoodslist`
- [`gds_u_datelist`](gds_u_datelist.md) — **일자별 신상품 날짜 목록 조회[사용자]** · `GET /gds/app/u_datelist`
- [`gds_u_delgoods`](gds_u_delgoods.md) — **상품 정보 삭제[사용자]** · `POST /gds/app/u_delgoods`
- [`gds_u_goods`](gds_u_goods.md) — **상품 상세 조회[사용자]** · `GET /gds/app/u_goods`
- [`gds_u_goodsclasslist`](gds_u_goodsclasslist.md) — **상품 카테고리 목록 조회[사용자]** · `GET /gds/app/u_goodsclasslist`
- [`gds_u_goodsclassspecalllist`](gds_u_goodsclassspecalllist.md) — **상품 카테고리 규격 목록 조회[사용자]** · `GET /gds/app/u_goodsclassspecalllist`
- [`gds_u_goodsskulist`](gds_u_goodsskulist.md) — **상품 규격 정보 조회[사용자]** · `GET /gds/app/u_goodsskulist`
- [`gds_u_imgsearchgoodslist`](gds_u_imgsearchgoodslist.md) — **이미지 상품 검색 목록[사용자]** · `POST /gds/app/u_imgsearchgoodslist`
- [`gds_u_recommendgoodslist`](gds_u_recommendgoodslist.md) — **상품 목록·범용[사용자]** · `GET /gds/app/u_recommendgoodslist`
- [`gds_u_searchgoodslist`](gds_u_searchgoodslist.md) — **상품 검색 목록 조회[사용자]** · `GET /gds/app/u_searchgoodslist`
- [`gds_u_selfgoodslist`](gds_u_selfgoodslist.md) — **셀프 추가 결제 상품 목록** · `GET /gds/app/u_selfgoodslist`
- [`gds_u_similargoodslist`](gds_u_similargoodslist.md) — **유사 상품 목록 조회[사용자]** · `GET /gds/app/u_similargoodslist`
- [`gds_u_storegoodslist`](gds_u_storegoodslist.md) — **매장 상품 목록 조회[사용자]** · `GET /gds/app/u_storegoodslist`

## 사용법

1. 필요한 엔드포인트 문서를 확인 (파일명 = 엔드포인트 이름)
2. `ids_*_login_*` 중 하나로 `access_token` 획득 (APM_USER_TOKEN 환경변수에 저장)
3. 요청 헤더에 `authcode: "HH " + $APM_USER_TOKEN` 추가
4. 해당 문서의 서명 규칙에 따라 `sign` 계산 후 호출

원본 문서: https://github.com/apmzoom-ai/apm-skills
