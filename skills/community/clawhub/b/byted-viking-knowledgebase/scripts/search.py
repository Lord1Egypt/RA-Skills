import json
import os

import requests
from volcengine.base.Request import Request

g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

service_id = os.getenv("VIKING_KBSVR_ID", "")
assert service_id, "VIKING_KBSVR_ID not set."

api_key = os.getenv("VIKING_KBSVR_API_KEY", "")
assert api_key, "VIKING_KBSVR_API_KEY not set."


def prepare_request(method, path, params=None, data=None, doseq=0):
    if params:
        for key in params:
            if (
                isinstance(params[key], int)
                or isinstance(params[key], float)
                or isinstance(params[key], bool)
            ):
                params[key] = str(params[key])
            elif isinstance(params[key], list):
                if not doseq:
                    params[key] = ",".join(params[key])
    r = Request()
    r.set_shema("http")
    r.set_method(method)
    r.set_connection_timeout(10)
    r.set_socket_timeout(10)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": g_knowledge_base_domain,
        "Authorization": f"Bearer {api_key}",
    }
    r.set_headers(headers)
    if params:
        r.set_query(params)
    r.set_host(g_knowledge_base_domain)
    r.set_path(path)
    if data is not None:
        r.set_body(json.dumps(data))
    return r


def knowledge_service_search(query: str):
    method = "POST"
    path = "/api/knowledge/service/chat"
    request_params = {
        "service_resource_id": service_id,
        "messages": [{"role": "user", "content": query}],
        "stream": False,
    }

    info_req = prepare_request(method=method, path=path, data=request_params)
    rsp = requests.request(
        method=info_req.method,
        url="http://{}{}".format(g_knowledge_base_domain, info_req.path),
        headers=info_req.headers,
        data=info_req.body,
    )
    rsp.encoding = "utf-8"
    rsp = rsp.json()

    if rsp.get("code") != 0:
        print(f"[Error] Search knowledge {query} got error response: {rsp}")
        return

    results = rsp.get("data", {}).get("result_list", [])
    if not results:
        print(
            f"[Warning] Search knowledge {query} got empty results. rsp: {rsp}"
        )
        return

    for result in results:
        print(result.get("content", ""))

    return


# def search_knowledge(
#     query: str,
#     index: str,
#     top_k: int = 5,
#     metadata: dict | None = None,
#     rerank: bool = True,
#     chunk_diffusion_count: int | None = 0,
#     project_name: str = "default",
#     region: str = "cn-beijing",
# ):
#     api_key = os.getenv("VIKING_KBSVR_API_KEY", "")

#     if not api_key:
#         print("[Error] VIKING_KBSVR_API_KEY not set.")
#         return

#     query_param = (
#         {
#             "doc_filter": {
#                 "op": "and",
#                 "conds": [
#                     {"op": "must", "field": str(k), "conds": [str(v)]}
#                     for k, v in metadata.items()
#                 ],
#             }
#         }
#         if metadata
#         else None
#     )

#     post_precessing = {
#         "rerank_swich": rerank,
#         "chunk_diffusion_count": chunk_diffusion_count,
#     }

#     viking_sdk_client = VikingKnowledgeBaseService(
#         host=f"api-knowledgebase.mlp.{region}.volces.com",
#         ak=ak,
#         sk=sk,
#         scheme="https",
#     )

#     response = viking_sdk_client.search_knowledge(
#         collection_name=index,
#         project=project_name,
#         query=query,
#         limit=top_k,
#         query_param=query_param,
#         post_processing=post_precessing,
#     )

#     # logger.debug(
#     #     f"Search knowledge {index} using project {project_name} original response: {response}"
#     # )

#     entries = []
#     if not response.get("result_list", []):
#         print(
#             f"[Warning] Search knowledge {index} using project {project_name} got empty response."
#         )
#         ...
#     else:
#         # logger.debug(
#         #     f"Search knowledge {index} using project {project_name} got {len(response.get('result_list', []))} results."
#         # )
#         for result in response.get("result_list", []):
#             doc_meta_raw_str = result.get("doc_info", {}).get("doc_meta")
#             doc_meta_list = (
#                 json.loads(doc_meta_raw_str) if doc_meta_raw_str else []
#             )
#             metadata = {}
#             for meta in doc_meta_list:
#                 metadata[meta["field_name"]] = meta["field_value"]

#             entries.append(
#                 {
#                     "content": result.get("content", ""),
#                     "metadata": metadata,
#                 }
#             )

#     print(entries)


# def search(
#     query: str,
#     index: str,
#     top_k: int = 5,
#     metadata: dict | None = None,
#     rerank: bool = True,
#     project_name: str = "default",
#     region: str = "cn-beijing",
# ):
#     search_knowledge(
#         query=query,
#         index=index,
#         top_k=top_k,
#         metadata=metadata,
#         rerank=rerank,
#         project_name=project_name,
#         region=region,
#     )


if __name__ == "__main__":
    import sys

    query = sys.argv[1]
    print(query)
    knowledge_service_search(query=query)
