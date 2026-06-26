#!/usr/bin/env node
import { asBool, parseArgs } from '../lib/args.mjs';
import { loadConnectionFromArgs } from '../lib/connection.mjs';
import {
  buildItemIdXml,
  callEwsOperation,
  ensureWriteConfirmed,
  parseDeleteType,
} from '../lib/ews-ops.mjs';

try {
  const args = parseArgs();
  ensureWriteConfirmed(args, 'DeleteItem');
  const conn = loadConnectionFromArgs(args);

  const itemId = args.itemId || args.id;
  if (!itemId) {
    throw new Error('itemId is required');
  }

  const deleteType = parseDeleteType(args.deleteType || process.env.EXCHANGE_DELETE_TYPE);
  const sendMeetingCancellations = args.sendMeetingCancellations || 'SendToNone';
  const suppressReadReceipts = asBool(args.suppressReadReceipts ?? true) ? 'true' : 'false';

  const bodyXml = `<m:DeleteItem DeleteType="${deleteType}" SendMeetingCancellations="${sendMeetingCancellations}" AffectedTaskOccurrences="AllOccurrences" SuppressReadReceipts="${suppressReadReceipts}">
      <m:ItemIds>
        ${buildItemIdXml(itemId, args.changeKey)}
      </m:ItemIds>
    </m:DeleteItem>`;

  if (asBool(args.dryRun)) {
    console.log(
      JSON.stringify(
        {
          dry_run: true,
          operation: 'DeleteItem',
          soap_action: 'http://schemas.microsoft.com/exchange/services/2006/messages/DeleteItem',
          soap_body_preview: bodyXml,
        },
        null,
        2
      )
    );
    process.exit(0);
  }

  await callEwsOperation({
    conn,
    operationName: 'DeleteItem',
    soapAction: 'http://schemas.microsoft.com/exchange/services/2006/messages/DeleteItem',
    bodyXml,
  });

  console.log(
    JSON.stringify(
      {
        ok: true,
        operation: 'DeleteItem',
        item_id: itemId,
        delete_type: deleteType,
      },
      null,
      2
    )
  );
} catch (err) {
  console.error('delete-item failed:', err.message);
  process.exit(1);
}
