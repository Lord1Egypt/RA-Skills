---
name: export-http-postman
description: Export an HTTP API endpoint from the current work project into a Postman-importable collection JSON file. Use when the user asks in Chinese or English to export an interface/API/HTTP endpoint, generate a Postman file, 导出接口, 导出http接口, 生成postman文件, or mentions the personal skill display name "导出接口Postman文件".
---

# 导出接口Postman文件

## Workflow

1. Identify the target endpoint from the user's wording.
   - Search the current project with `rg` for controller paths, route decorators, servlet mappings, OpenAPI annotations, Feign clients, or framework-specific HTTP route declarations.
   - Preserve the project's existing path variables, query names, request body field names, headers, and content type.
   - If several endpoints match and choosing the wrong one would change behavior, ask one concise clarification question.

2. Infer the service name and domain.
   - Prefer project metadata such as `spring.application.name`, module/service directory name, deployment config, or gateway route config.
   - Read `references/domains.md` for the stored domain list. Do not read `C:\Windows\System32\drivers\etc\hosts` during ordinary endpoint exports.
   - Recommend the stored domain whose hostname contains or closely resembles the service name. If multiple domains are plausible, choose the best match and mention the alternatives in the final response.
   - If no good domain is found, or the endpoint appears to belong to a new service not present in `references/domains.md`, ask the user for the domain before generating the final Postman file.
   - After the user provides a new service domain, persist it immediately in `references/domains.md` before generating the Postman file. Prefer `scripts/create_postman_collection.py --service <service-name> --domain <domain> --remember-domain` so future exports can reuse the answer.
   - Treat `references/domains.md` as the durable memory for service/domain answers. Do not rely only on chat history.

3. Build a Postman collection.
   - Use Postman Collection v2.1 JSON.
   - Prefer `scripts/create_postman_collection.py` to generate the collection shell, then patch the JSON only for details the script cannot express cleanly.
   - Include method, URL, query params, path variables, headers, and an example JSON body when they can be inferred from code.
   - Use placeholders for values that are environment-specific or sensitive, such as tokens, cookies, user IDs, order IDs, trace IDs, and timestamps.
   - Do not include secrets found in local config files.

4. Save the deliverable.
   - In projectless chats, save user-facing files under the configured `outputs` directory.
   - In repository work, save the generated Postman JSON in a location the user requested; otherwise use the current workspace or a clear output directory.
   - Name the file after the service and endpoint, for example `order-create-postman-collection.json`.

5. Validate before finishing.
   - Run `python scripts/create_postman_collection.py --help` if the script was changed.
   - Parse the generated JSON with Python or another JSON parser.
   - Report the output file, chosen base URL/domain, inferred endpoint, and any assumptions.

## Script Usage

From this skill directory:

```bash
python scripts/create_postman_collection.py \
  --name "Service endpoint" \
  --method POST \
  --base-url "https://example.company.com" \
  --path "/api/example/{id}" \
  --query "debug=false" \
  --header "Content-Type: application/json" \
  --body-json-file "request-body.json" \
  --output "example-postman-collection.json"
```

Use `--domains references/domains.md --service <service-name> --print-domain-candidates` to inspect stored domain candidates.

Use `--domains references/domains.md --service <service-name> --domain <domain> --remember-domain` after the user answers a missing-domain question.
