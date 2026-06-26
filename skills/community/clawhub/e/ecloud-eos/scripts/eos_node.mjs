#!/usr/bin/env node
/**
 * 移动云 EOS Node.js SDK 操作脚本
 *
 * 依赖：npm install @aws-sdk/client-s3
 * 凭证通过环境变量读取：EOS_ACCESS_KEY, EOS_SECRET_KEY, EOS_REGION, EOS_BUCKET, EOS_ENDPOINT
 *
 * 用法：node eos_node.mjs <action> [options]
 */

import { S3Client, PutObjectCommand, GetObjectCommand, ListObjectsCommand, DeleteObjectCommand, HeadObjectCommand, GetObjectAclCommand, GetBucketAclCommand, PutObjectAclCommand, PutBucketAclCommand, CreateMultipartUploadCommand, UploadPartCommand, CompleteMultipartUploadCommand, AbortMultipartUploadCommand, CreateBucketCommand, DeleteBucketCommand, ListBucketsCommand, CopyObjectCommand, PutBucketPolicyCommand, GetBucketPolicyCommand, DeleteBucketPolicyCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import fs from 'fs';
import path from 'path';

// 从环境变量读取配置
const SecretId = process.env.EOS_ACCESS_KEY;
const SecretKey = process.env.EOS_SECRET_KEY;
const Region = process.env.EOS_REGION;
const Endpoint = process.env.EOS_ENDPOINT;
const EOS_Bucket = process.env.EOS_BUCKET;

const s3Config = {
    credentials: {
        accessKeyId: SecretId,
        secretAccessKey: SecretKey,
    },
    endpoint: Endpoint,
    region: Region,
}

const client = new S3Client(s3Config);

// 解析命令行参数
function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        result[key] = next;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  return result;
}

// 输出 JSON 结果
function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

// ========== 辅助函数 ==========

async function uploadMultipart(filePath, key, bucket) {
  const PART_SIZE = 5 * 1024 * 1024; // 5MB
  const fileBuffer = fs.readFileSync(filePath);
  const uploadId = (await client.send(new CreateMultipartUploadCommand({
    Bucket: bucket,
    Key: key,
  }))).UploadId;

  const parts = [];
  const partCount = Math.ceil(fileBuffer.length / PART_SIZE);

  for (let i = 0; i < partCount; i++) {
    const start = i * PART_SIZE;
    const end = Math.min(start + PART_SIZE, fileBuffer.length);
    const part = await client.send(new UploadPartCommand({
      Bucket: bucket,
      Key: key,
      UploadId: uploadId,
      PartNumber: i + 1,
      Body: fileBuffer.subarray(start, end),
    }));
    parts.push({ ETag: part.ETag, PartNumber: i + 1 });
    console.log(`Part ${i + 1}/${partCount} uploaded`);
  }

  await client.send(new CompleteMultipartUploadCommand({
    Bucket: bucket,
    Key: key,
    UploadId: uploadId,
    MultipartUpload: { Parts: parts },
  }));
}

async function uploadSmall(filePath, key, bucket) {
  const fileBuffer = fs.readFileSync(filePath);
  await client.send(new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    Body: fileBuffer,
  }));
}

// ========== 操作实现 ==========

async function upload(opts, positionalArgs) {
  // 支持位置参数：第一个是文件路径，第二个是 key
  const filePath = opts.file || positionalArgs[0];
  let key = opts.key || positionalArgs[1] || path.basename(filePath);

  // 将 Windows 路径分隔符转换为正斜杠（对象存储 key 使用正斜杠）
  key = key.replace(/\\/g, '/');

  if (!filePath) {
    throw new Error('缺少文件路径参数，请使用 --file <path> 或直接提供路径');
  }
  if (!fs.existsSync(filePath)) {
    throw new Error(`文件不存在：${filePath}`);
  }

  const stats = fs.statSync(filePath);
  const LARGE_FILE_THRESHOLD = 500 * 1024 * 1024; // 500MB

  try {
    if (stats.size > LARGE_FILE_THRESHOLD) {
      await uploadMultipart(filePath, key, EOS_Bucket);
    } else {
      await uploadSmall(filePath, key, EOS_Bucket);
    }

    output({
      success: true,
      action: 'upload',
      key: key,
      filePath: filePath,
      size: stats.size,
      message: '文件上传成功'
    });
  } catch (err) {
    throw err;
  }
}

async function download(opts) {
  const key = opts.key;
  const outputPath = opts.output || path.basename(key);

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: normalizedKey,
  };

  try {
    const command = new GetObjectCommand(input);
    const response = await client.send(command);
    const str = await response.Body.transformToByteArray();
    fs.writeFileSync(outputPath, str);
    output({
      success: true,
      action: 'download',
      key: key,
      outputPath: outputPath,
      message: '文件下载成功'
    });
  } catch (err) {
    throw err;
  }
}

async function copyFile(opts) {
  const sourceKey = opts['source-key'];
  const destKey = opts['dest-key'];
  const destBucket = opts['dest-bucket'];

  if (!sourceKey) {
    throw new Error('缺少 --source-key 参数（源文件路径）');
  }
  if (!destKey) {
    throw new Error('缺少 --dest-key 参数（目标文件路径）');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedSourceKey = sourceKey.replace(/\\/g, '/');
  const normalizedDestKey = destKey.replace(/\\/g, '/');

  const targetBucket = destBucket || EOS_Bucket;

  try {
    const input = {
      Bucket: targetBucket,
      CopySource: `${EOS_Bucket}/${normalizedSourceKey}`,
      Key: normalizedDestKey,
    };

    const command = new CopyObjectCommand(input);
    const response = await client.send(command);

    output({
      success: true,
      action: 'copy-file',
      sourceKey: normalizedSourceKey,
      sourceBucket: EOS_Bucket,
      destKey: normalizedDestKey,
      destBucket: targetBucket,
      message: '文件复制成功'
    });
  } catch (err) {
    throw err;
  }
}

async function list(opts) {
  let prefix = opts.prefix || '';
  const maxKeys = Math.min(parseInt(opts['max-keys'], 10) || 100, 100);
  let marker = opts.marker;

  // 将 Windows 路径分隔符转换为正斜杠
  if (prefix) {
    prefix = prefix.replace(/\\/g, '/');
  }
  if (marker) {
    marker = marker.replace(/\\/g, '/');
  }

  const input = {
    Bucket: EOS_Bucket,
    Prefix: prefix,
    MaxKeys: maxKeys,
  };

  // 如果有 marker，添加到请求中（旧版 API 使用 Marker）
  if (marker) {
    input.Marker = marker;
  }

  try {
    const command = new ListObjectsCommand(input);
    const response = await client.send(command);

    output({
      success: true,
      action: 'list',
      prefix: prefix,
      maxKeys: maxKeys,
      marker: marker || null,
      nextMarker: response.NextMarker || null,
      isTruncated: response.IsTruncated || false,
      count: response.Contents ? response.Contents.length : 0,
      data: response
    });
  } catch (err) {
    throw err;
  }
}

async function deleteObject(opts) {
  const key = opts.key;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: normalizedKey,
  };

  try {
    const command = new DeleteObjectCommand(input);
    const response = await client.send(command);
    output({
      success: true,
      action: 'delete',
      key: key,
      message: '文件删除成功'
    });
  } catch (err) {
    throw err;
  }
}

async function head(opts) {
  const key = opts.key;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: normalizedKey,
  };

  try {
    const command = new HeadObjectCommand(input);
    const response = await client.send(command);
    output({
      success: true,
      action: 'head',
      key: key,
      data: response
    });
  } catch (err) {
    throw err;
  }
}

async function exists(opts) {
  const key = opts.key;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: normalizedKey,
  };

  try {
    const command = new HeadObjectCommand(input);
    await client.send(command);
    output({
      success: true,
      action: 'exists',
      key: key,
      exists: true,
      message: '文件存在'
    });
  } catch (err) {
    if (err.name === 'NotFound' || err.$metadata?.httpStatusCode === 404) {
      output({
        success: true,
        action: 'exists',
        key: key,
        exists: false,
        message: '文件不存在'
      });
    } else {
      throw err;
    }
  }
}

async function acl(opts) {
  const key = opts.key;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: normalizedKey,
  };

  try {
    const command = new GetObjectAclCommand(input);
    const response = await client.send(command);
    output({
      success: true,
      action: 'acl',
      key: key,
      data: response
    });
  } catch (err) {
    throw err;
  }
}

async function bucketAcl(opts) {
  const input = {
    Bucket: EOS_Bucket,
  };

  try {
    const command = new GetBucketAclCommand(input);
    const response = await client.send(command);
    output({
      success: true,
      action: 'get-bucket-acl',
      bucket: EOS_Bucket,
      data: response
    });
  } catch (err) {
    throw err;
  }
}

async function setAcl(opts) {
  const key = opts.key;
  const acl = opts.acl;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  if (!acl) {
    throw new Error('缺少 --acl 参数（支持的值：private、public-read、public-read-write）');
  }

  // 验证 acl 值
  const validAclValues = ['private', 'public-read', 'public-read-write'];
  if (!validAclValues.includes(acl)) {
    throw new Error(`--acl 参数值无效，支持的值：${validAclValues.join(', ')}`);
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  try {
    const input = {
      Bucket: EOS_Bucket,
      Key: normalizedKey,
      ACL: acl,
    };

    const command = new PutObjectAclCommand(input);
    await client.send(command);
    output({
      success: true,
      action: 'set-acl',
      key: key,
      acl: acl,
      message: '文件权限设置成功'
    });
  } catch (err) {
    throw err;
  }
}

async function setBucketAcl(opts) {
  const acl = opts.acl;

  if (!acl) {
    throw new Error('缺少 --acl 参数（支持的值：private、public-read、public-read-write）');
  }

  // 验证 acl 值
  const validAclValues = ['private', 'public-read', 'public-read-write'];
  if (!validAclValues.includes(acl)) {
    throw new Error(`--acl 参数值无效，支持的值：${validAclValues.join(', ')}`);
  }

  try {
    const input = {
      Bucket: EOS_Bucket,
      ACL: acl,
    };

    const command = new PutBucketAclCommand(input);
    await client.send(command);
    output({
      success: true,
      action: 'set-bucket-acl',
      bucket: EOS_Bucket,
      acl: acl,
      message: '桶权限设置成功'
    });
  } catch (err) {
    throw err;
  }
}

async function createBucket(opts) {
  const bucket = opts.bucket;

  if (!bucket) {
    throw new Error('缺少 --bucket 参数');
  }

  try {
    const input = {
      Bucket: bucket,
    };

    const command = new CreateBucketCommand(input);
    await client.send(command);
    output({
      success: true,
      action: 'create-bucket',
      bucket: bucket,
      message: '桶创建成功'
    });
  } catch (err) {
    throw err;
  }
}

async function deleteBucket(opts) {
  const bucket = opts.bucket;

  if (!bucket) {
    throw new Error('缺少 --bucket 参数');
  }

  try {
    // 先检查桶是否为空
    const listInput = {
      Bucket: bucket,
      MaxKeys: 1,
    };

    const listCommand = new ListObjectsCommand(listInput);
    const listResponse = await client.send(listCommand);

    // 如果桶中有文件，返回错误提示
    if (listResponse.Contents && listResponse.Contents.length > 0) {
      throw new Error(`桶 ${bucket} 不为空，无法删除。请先使用 empty-bucket 命令清空桶内的所有文件。注意：清空桶是高危操作，需要使用 --confirm 参数确认。`);
    }

    // 桶为空，执行删除操作
    const deleteInput = {
      Bucket: bucket,
    };

    const deleteCommand = new DeleteBucketCommand(deleteInput);
    await client.send(deleteCommand);
    output({
      success: true,
      action: 'delete-bucket',
      bucket: bucket,
      message: '桶删除成功'
    });
  } catch (err) {
    throw err;
  }
}

async function emptyBucket(opts) {
  const bucket = opts.bucket;

  if (!bucket) {
    throw new Error('缺少 --bucket 参数');
  }

  // 检查是否有确认参数
  if (!opts.confirm && !opts.force) {
    throw new Error(`清空桶是高危操作，将删除桶内的所有文件。请使用 --confirm 参数确认此操作。示例：node scripts/eos_node.mjs empty-bucket --bucket ${bucket} --confirm`);
  }

  try {
    // 获取桶内所有文件（使用分页获取）
    const allObjects = [];
    let marker = null;

    do {
      const listInput = {
        Bucket: bucket,
        MaxKeys: 100,
      };

      if (marker) {
        listInput.Marker = marker;
      }

      const listCommand = new ListObjectsCommand(listInput);
      const listResponse = await client.send(listCommand);

      if (listResponse.Contents && listResponse.Contents.length > 0) {
        allObjects.push(...listResponse.Contents);
      }

      marker = listResponse.NextMarker || null;
    } while (marker);

    // 如果桶为空，直接返回
    if (allObjects.length === 0) {
      output({
        success: true,
        action: 'empty-bucket',
        bucket: bucket,
        deletedCount: 0,
        message: '桶已为空，无需删除文件'
      });
      return;
    }

    // 逐个删除文件
    let deletedCount = 0;
    let failedCount = 0;
    const errors = [];

    for (const obj of allObjects) {
      try {
        const deleteInput = {
          Bucket: bucket,
          Key: obj.Key,
        };

        const deleteCommand = new DeleteObjectCommand(deleteInput);
        await client.send(deleteCommand);
        deletedCount++;
      } catch (err) {
        failedCount++;
        errors.push({ key: obj.Key, error: err.message });
      }
    }

    output({
      success: true,
      action: 'empty-bucket',
      bucket: bucket,
      deletedCount: deletedCount,
      failedCount: failedCount,
      message: `清空桶完成，成功删除 ${deletedCount} 个文件${failedCount > 0 ? `，失败 ${failedCount} 个` : ''}`,
      errors: failedCount > 0 ? errors : undefined
    });
  } catch (err) {
    throw err;
  }
}

async function setBucket(opts) {
  const bucket = opts.bucket;

  if (!bucket) {
    throw new Error('缺少 --bucket 参数');
  }

  // 由于现在使用环境变量存储配置，set-bucket 功能已移至 setup 脚本
  output({
    success: false,
    action: 'set-bucket',
    error: 'set-bucket 功能已移至 setup 脚本',
    message: '请使用 setup 脚本切换桶：',
    instructions: {
      windows: 'scripts\\setup.ps1 -SetBucket <bucket>',
      linux_macos: 'scripts/setup.sh --set-bucket <bucket>'
    },
    note: '切换桶后需要重新启动终端或重新设置环境变量才能生效'
  });
}

async function setReferer(opts) {
  const referers = opts.referers;
  const refererType = opts.type || 'allow'; // allow 或 deny

  if (!referers) {
    throw new Error('缺少 --referers 参数（防盗链白名单，用逗号分隔，使用 * 表示所有域名）');
  }

  // 验证 type 参数
  if (!['allow', 'deny'].includes(refererType)) {
    throw new Error('--type 参数值无效，支持的值：allow（白名单）或 deny（黑名单）');
  }

  try {
    // 构建 Bucket Policy
    const refererList = referers.split(',').map(r => r.trim());
    const effect = refererType === 'allow' ? 'Allow' : 'Deny';

    const policy = {
      Version: "2012-10-17",
      Statement: [
        {
          Sid: "RefererPolicy",
          Effect: effect,
          Principal: "*",
          Action: "s3:GetObject",
          Resource: `arn:aws:s3:::${EOS_Bucket}/*`,
          Condition: {
            StringLike: {
              "aws:Referer": refererList
            }
          }
        }
      ]
    };

    const input = {
      Bucket: EOS_Bucket,
      Policy: JSON.stringify(policy),
    };

    const command = new PutBucketPolicyCommand(input);
    await client.send(command);

    output({
      success: true,
      action: 'set-referer',
      bucket: EOS_Bucket,
      type: refererType,
      referers: refererList,
      message: '防盗链设置成功'
    });
  } catch (err) {
    throw err;
  }
}

async function getReferer(opts) {
  try {
    const input = {
      Bucket: EOS_Bucket,
    };

    const command = new GetBucketPolicyCommand(input);
    const response = await client.send(command);

    const policy = JSON.parse(response.Policy);
    const refererStatement = policy.Statement.find(s => s.Sid === "RefererPolicy" && s.Condition?.StringLike?.["aws:Referer"]);

    if (refererStatement) {
      output({
        success: true,
        action: 'get-referer',
        bucket: EOS_Bucket,
        type: refererStatement.Effect.toLowerCase(),
        referers: refererStatement.Condition.StringLike["aws:Referer"],
        message: '防盗链查询成功'
      });
    } else {
      output({
        success: true,
        action: 'get-referer',
        bucket: EOS_Bucket,
        message: '未设置防盗链'
      });
    }
  } catch (err) {
    if (err.name === 'NoSuchBucketPolicy' || err.$metadata?.httpStatusCode === 404) {
      output({
        success: true,
        action: 'get-referer',
        bucket: EOS_Bucket,
        message: '未设置防盗链'
      });
    } else {
      throw err;
    }
  }
}

async function deleteReferer(opts) {
  try {
    const input = {
      Bucket: EOS_Bucket,
    };

    const command = new DeleteBucketPolicyCommand(input);
    await client.send(command);

    output({
      success: true,
      action: 'delete-referer',
      bucket: EOS_Bucket,
      message: '防盗链已删除'
    });
  } catch (err) {
    if (err.name === 'NoSuchBucketPolicy' || err.$metadata?.httpStatusCode === 404) {
      throw new Error('该桶未设置防盗链，无需删除');
    } else {
      throw err;
    }
  }
}

async function listBuckets() {
  try {
    const command = new ListBucketsCommand({});
    const response = await client.send(command);

    const buckets = response.Buckets || [];
    const bucketList = buckets.map(bucket => ({
      name: bucket.Name,
      creationDate: bucket.CreationDate
    }));

    output({
      success: true,
      action: 'list-buckets',
      count: bucketList.length,
      buckets: bucketList,
      message: `找到 ${bucketList.length} 个存储桶`
    });
  } catch (err) {
    throw err;
  }
}

async function generateUrl(opts) {
  const key = opts.key;
  const expires = parseInt(opts.expires, 10) || 3600;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  // 将 Windows 路径分隔符转换为正斜杠
  const normalizedKey = key.replace(/\\/g, '/');

  const input = {
    Bucket: EOS_Bucket,
    Key: key,
  };

  try {
    const command = new GetObjectCommand(input);
    const url = await getSignedUrl(client, command, { expiresIn: expires });
    output({
      success: true,
      action: 'generate-url',
      key: key,
      url: url,
      expiresIn: expires,
      expiresAt: new Date(Date.now() + expires * 1000).toISOString(),
      message: '文件共享外链生成成功'
    });
  } catch (err) {
    throw err;
  }
}

// ========== 主入口 ==========

const args = process.argv.slice(2);
const action = args[0];
const opts = parseArgs(args.slice(1));

// 检查必要环境变量，但允许特定操作在缺失桶名时执行
if (!SecretId || !SecretKey || !Region || !Endpoint) {
  console.error(JSON.stringify({
    success: false,
    error: '环境变量中缺少必要的凭证信息，请运行 setup 脚本配置',
    missing: !SecretId ? 'EOS_ACCESS_KEY' : !SecretKey ? 'EOS_SECRET_KEY' : !Region ? 'EOS_REGION' : 'EOS_ENDPOINT',
  }));
  process.exit(1);
}

// 检查桶名环境变量，但允许特定操作在缺失时执行
const bucketRequiredActions = ['list-objects', 'get-bucket-acl', 'set-bucket-acl', 'set-referer', 'get-referer', 'delete-referer', 'empty-bucket', 'set-bucket'];
const bucketOptionalActions = ['list-buckets', 'create-bucket', 'delete-bucket'];

if (!EOS_Bucket && bucketRequiredActions.includes(action)) {
  console.error(JSON.stringify({
    success: false,
    error: '环境变量中缺少桶名信息，请运行 setup 脚本配置或切换桶',
    missing: 'EOS_BUCKET',
  }));
  process.exit(1);
}

const actions = {
  'list-buckets': listBuckets,
  'create-bucket': createBucket,
  'delete-bucket': deleteBucket,
  'empty-bucket': emptyBucket,
  'set-bucket': setBucket,
  'get-bucket-acl': bucketAcl,
  'set-bucket-acl': setBucketAcl,
  'set-referer': setReferer,
  'get-referer': getReferer,
  'delete-referer': deleteReferer,
  'upload-object': upload,
  'download-object': download,
  'copy-object': copyFile,
  'list-objects': list,
  'delete-object': deleteObject,
  'head-object': head,
  'exists-object': exists,
  'get-object-acl': acl,
  'set-object-acl': setAcl,
  'generate-url': generateUrl,
};

if (!action || !actions[action]) {
  output({
    success: false,
    error: `未知操作：${action || '(空)'}`,
    availableActions: Object.keys(actions),
    usage: 'node eos_node.mjs <action> [--option value ...]',
  });
  process.exit(1);
}

try {
  // 提取位置参数（不以 -- 开头的参数）
  const positionalArgs = process.argv.slice(2).filter(arg => !arg.startsWith('--'));
  // 移除 action 本身
  positionalArgs.shift();

  await actions[action](opts, positionalArgs);
} catch (err) {
  output({
    success: false,
    action,
    error: err.message || String(err),
    code: err.code,
  });
  process.exit(1);
}