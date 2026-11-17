export function formatMarkdown(data) {
  if (data?.status === 'queued' || data?.status === 'running' || data?.pending) {
    return `## Search pending\n\nStatus: ${data.status ?? 'pending'}${data.request_id ? `\nRequest ID: ${data.request_id}` : ''}${data.idempotency_key ? `\nIdempotency key: ${data.idempotency_key}` : ''}\n\nThe search is still processing. Reuse the same idempotency key to recover its outcome.`
  }
  const rows = Array.isArray(data?.organic) ? data.organic : []
  const out = [`## Search results`, '', `Query: ${data?.search_parameters?.q ?? ''}`, '']
  if (data?.quality?.warnings?.includes('source_scope_not_satisfied')) {
    out.push(`Warning: Requested source coverage was not satisfied. ${data.quality.original ?? 0} upstream result(s) were checked; none matched the requested scope.`, '')
  }
  for (const item of rows) {
    out.push(`${item.position ?? ''}. [${item.title ?? 'Untitled'}](${item.link ?? ''})`)
    if (item.snippet) out.push(`   ${item.snippet}`)
  }
  if (!rows.length) out.push('No organic results were returned.')
  out.push('', '### Sources', '')
  rows.forEach((item, i) => out.push(`${i + 1}. [${item.title ?? item.link}](${item.link})${item.link_type === 'redirect' ? ' (redirect link)' : ''}`))
  return out.join('\n')
}
