# FTM Development Reference

## ACE CLI Commands
```bash
mqsicreatebar -data <workspace> -b MyApp.bar -a MyApp_PhysTrans MyApp_Mappers MyApp_Actions
mqsideploy -i <host> -p <port> -e <exec_group> -a MyApp.bar
mqsilist <broker_name>
mqsistart <broker_name> / mqsistop <broker_name>
mqsireadlog <broker_name> | mqsiformatlog
mqsichangetrace <broker_name> -e <eg> -f <flow> -l debug -r
```

## RSA Workflow
1. Define Application + Version
2. Create Service Participants + Channels (with Format and Mapper refs)
3. Model FSM State Machines per object subtype (using FTM plugin stereotypes)
4. Define Scheduler Tasks + Calendar Groups (if time-based patterns used)
5. Export: Right-click → FTM → Export Configuration → SQL scripts
6. Deploy: `db2 -tvf <script>.sql`

## DB2 Operational Queries
```sql
-- Find stuck transactions
SELECT O.ID, O.STATE, O.SUBTYPE, O.LAST_UPDATED_TS
FROM OBJ_BASE O
WHERE O.LAST_UPDATED_TS < CURRENT TIMESTAMP - 1 HOUR
  AND O.STATE NOT IN ('S_Completed', 'S_Cancelled');

-- Find alert states
SELECT O.ID, O.STATE, O.SUBTYPE, O.CREATED_TS
FROM OBJ_BASE O WHERE O.STATE LIKE '%Failed%' OR O.STATE LIKE '%Alert%';

-- Check unprocessed events
SELECT COUNT(*), E.EVENT_TYPE_NAME FROM EVENT_BASE E
WHERE E.PROCESSED = 'N' GROUP BY E.EVENT_TYPE_NAME;

-- Check FSM transitions for a state
SELECT T.FROM_STATE, T.EVENT_TYPE, T.FSM_ACTION, T.TO_STATE
FROM FSM_TRANSITION T JOIN FSM F ON T.FSM_ID = F.ID
WHERE T.FROM_STATE = 'S_WaitingForCoreBankingResponse';

-- Check object relationships
SELECT R.FROM_OBJ_ID, R.TO_OBJ_ID, R.REL_TYPE
FROM OBJ_OBJ_REL R WHERE R.FROM_OBJ_ID = '<txn_id>';

-- Check effective version
SELECT APP_ID, VERSION_ID, EFFECTIVE FROM APP_VERSION;
```

## MQ Commands
```bash
echo "DIS QL(FTM.EVENT.QUEUE) CURDEPTH IPPROCS" | runmqsc <QMGR>
amqsbcg <QUEUE_NAME> <QMGR>   # browse messages
echo "DIS QL(SYSTEM.DEAD.LETTER.QUEUE) CURDEPTH" | runmqsc <QMGR>
```

## Docker Debug
```bash
docker logs <ace_container> -f
docker exec <ace_container> mqsilist
docker exec -it <db2_container> bash -c "su - db2inst1 -c 'db2 connect to FTMDB'"
docker exec <mq_container> bash -c "echo 'DIS QL(FTM.EVENT.QUEUE) CURDEPTH' | /opt/mqm/bin/runmqsc FTMQMGR"
```

## Common Issues

### Transaction stuck in a state
1. Query `OBJ_BASE` — check `STATE`, `LAST_UPDATED_TS`
2. Check MQ event queue depth
3. Check `EVENT_BASE` for unprocessed events
4. Check `FSM_TRANSITION` for expected events in current state
5. Run `mqsireadlog | mqsiformatlog` for ACE errors
6. Check `SERVICE_PARTICIPANT_BASE` — is target SP ACTIVE?
7. Check `OBJ_OBJ_REL` for correlation issues

### Mapping failure (E_MpInMappingAborted)
1. Check ACE broker logs for ESQL/WTX error line
2. Verify ISF namespace is `http://www.ibm.com/xmlns/prod/ftm/isf/v3`
3. Check for missing `xsi:type` on polymorphic ISF elements
4. Check Currency is set as attribute, not text content
5. Check for empty optional elements that weren't deleted

### MQ queue not draining
1. Check ACE execution group: `mqsilist <broker> -e <eg>`
2. Check DB2 connectivity from ACE
3. Check backout threshold — messages may be in DLQ
