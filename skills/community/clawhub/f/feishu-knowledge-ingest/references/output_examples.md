# Output examples

## kb-items.jsonl example
{"batch_id":"ingest-20260323-081200-a7f3","source_file":"SSL VPN 连接操作说明.docx","source_token":"file_xxx","file_type":"docx","topic":"vpn access","content_type":"sop","summary":"Explains prerequisites, client install, and login steps for SSL VPN.","extracted_at":"2026-03-23T08:12:00Z","confidence":0.86}

## failed-items.jsonl example
{"batch_id":"ingest-20260323-081200-a7f3","source_file":"IT资产管理制度.pdf","source_token":"file_yyy","file_type":"pdf","failure_reason":"parse_error","error_detail":"empty extracted text","suggested_action":"retry with OCR or confirm if the PDF is image-based","failed_at":"2026-03-23T08:12:05Z"}

## MEMORY.candidate.md sections
- Batch header
- Candidate topics
- Candidate summaries
- Source references
- Confidence and review notes
