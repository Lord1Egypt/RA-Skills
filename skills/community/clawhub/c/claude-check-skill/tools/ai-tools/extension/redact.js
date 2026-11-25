function redactedKyc(data) {
  const known=new Set(['not_required','pending','approved','denied']);
  return ['KYC 查询 · '+data.checkedAt,...data.rows.map((row,i)=>{
    const code=row.error?.match(/HTTP (\d{3})/)?.[1];
    return `组织 ${i+1}: ${row.error?(code?'HTTP '+code:'查询失败'):(known.has(row.status)?row.status:'未知状态')}`;
  }),...(data.incomplete?['部分组织未查询，结果不完整。']:[]),'当前无需验证不等于已通过 KYC；多组织结果不能代表当前选择或整个账号安全。'].join('\n');
}
