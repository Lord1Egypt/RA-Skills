"""Private reasons are read from stdin and sent to the Registry; local retry records contain identifiers and a reason digest, never the reason text."""
import hashlib
import re
import sys
import unicodedata
import urllib.parse
import uuid

UUID=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

def run(r,o):
    action=o.group_command
    r.fail(action in ('submit','list','show'),'INVALID_ARGUMENT','Use reports submit, list or show.',2)
    r.fail(not (o.session or o.name or o.slug or o.description or o.theme or o.query or o.alias),
           'INVALID_ARGUMENT','Group options do not apply to reports.',2)
    r.fail(action=='list' or not o.after,'INVALID_ARGUMENT','--after applies only to list.',2)
    if o.after:r.fail(re.fullmatch(UUID,o.after),'INVALID_ARGUMENT','Use a request UUID for --after.',2)
    r.fail(action=='submit' or not (o.reason_stdin or o.request_id),'INVALID_ARGUMENT','Reason and request ID apply only to submit.',2)
    if action=='list':r.fail(not o.group_id,'INVALID_ARGUMENT','List takes no positional argument.',2)
    else:r.fail(o.group_id and re.fullmatch(UUID,o.group_id),'INVALID_ARGUMENT','Use the exact group or request UUID.',2)
    if o.request_id:r.fail(re.fullmatch(UUID,o.request_id),'INVALID_ARGUMENT','Use a UUID for --request-id.',2)
    with r.locked():
        state=r.read();r.fail(state and state['state']=='active','NOT_ENROLLED','An active local registration is required.')
        host=state['host_id'];r.transport_ready()
        if action!='submit':
            query=urllib.parse.urlencode({'after':o.after}) if o.after else ''
            data=r.request('reports'+('/'+o.group_id if action=='show' else ''),host,query=query,raw_result=True)
            return 'OK','Private removal request information retrieved.',data
        r.fail(o.reason_stdin,'INVALID_ARGUMENT','Provide the reason through --reason-stdin; do not put private text in arguments.',2)
        raw=sys.stdin.buffer.read(16385)
        try:reason=raw.decode('utf-8')
        except UnicodeError:raise r.cli.Failure('INVALID_REPORT_TEXT','Use UTF-8 text.',2) from None
        r.fail(len(raw)<=16384 and 0<len(reason)<=4000 and reason.strip() and
               all(c in '\r\n\t' or unicodedata.category(c) not in ('Cc','Cf','Cs') for c in reason),
               'INVALID_REPORT_TEXT','Use 1–4,000 characters, at most 16 KiB, without unsafe control characters.',2)
        import clawreef_groups as storage
        path=r.directory/('report-'+hashlib.sha256((r.service+host+o.group_id).encode()).hexdigest()+'.json')
        old=storage.private_json(r,path)
        digest=hashlib.sha256(raw).hexdigest()
        if old and not o.request_id:
            r.fail(old.get('schema_version')==1 and old.get('service')==r.service and old.get('host_id')==host and old.get('key_id')==r.key_id and old.get('group_id')==o.group_id,
                   'INVALID_OPERATION','Saved request belongs to a different registration.')
            r.fail(old.get('reason_digest')==digest,'IDEMPOTENCY_CONFLICT','Saved request used a different reason. Reuse its original text, or select a new --request-id UUID.',3)
            request_id=old.get('request_id')
        else:request_id=o.request_id or str(uuid.uuid4())
        r.fail(isinstance(request_id,str) and re.fullmatch(UUID,request_id),'INVALID_OPERATION','Invalid saved request ID.')
        storage.atomic(path,dict(schema_version=1,service=r.service,host_id=host,key_id=r.key_id,group_id=o.group_id,request_id=request_id,reason_digest=digest))
        try:
            data=r.request('reports',host,{'id':request_id,'group_id':o.group_id,'reason':reason},r.http.operation_id(),raw_result=True)
        except r.cli.Failure as e:
            e.data={'request_id':request_id,'group_id':o.group_id}
            e.next_action='Inspect reports show '+request_id+'; retry submission with the same --request-id and original reason via stdin.'
            raise
        return 'REPORT_SUBMITTED','Removal request recorded. This does not remove the group.',data
