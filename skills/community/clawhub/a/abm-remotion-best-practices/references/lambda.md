# Remotion Lambda Rendering

Overview of serverless video rendering on AWS Lambda for scaling beyond local rendering.

## What is Remotion Lambda?

Remotion Lambda renders videos on AWS Lambda functions. Each Lambda invocation renders a chunk of frames in parallel, then stitches the result. This enables:

- **Faster renders** -- parallel frame rendering across multiple Lambda instances
- **Batch processing** -- render many videos without tying up a local machine
- **Scalability** -- render hundreds of videos concurrently

## When to Use

| Scenario | Local Render | Lambda |
|----------|-------------|--------|
| Single video, development | Best choice | Overkill |
| Single video, production | Good | Optional |
| Batch of 10+ videos | Slow | Best choice |
| CI/CD pipeline rendering | Limited | Best choice |
| Personalized videos at scale | Not feasible | Best choice |

**Default to local rendering.** Use Lambda when you need parallelism or batch processing.

## Setup Requirements

### AWS Credentials

Lambda rendering requires three environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export REMOTION_AWS_REGION="us-east-1"
```

### Package Installation

```bash
npm install @remotion/lambda
```

Ensure the version matches your other `@remotion/*` packages.

## 3-Step Deploy Flow

### Step 1: Deploy Lambda Function

```bash
npx remotion lambda functions deploy
```

Creates the Lambda function in your AWS account. Run once per region.

### Step 2: Deploy Site (Upload Bundle)

```bash
npx remotion lambda sites create src/index.ts
```

Bundles your Remotion project and uploads it to S3. Returns a serve URL. Run after each code change.

### Step 3: Render

```bash
npx remotion lambda render --function-name <fn> --serve-url <url> CompositionId
```

Triggers a Lambda render. Returns a URL to the rendered video in S3.

### Check Render Status

```bash
npx remotion lambda renders list
```

Lists active and completed renders with status and output URLs.

## Cost Considerations

- **Lambda charges**: Per invocation + per millisecond of execution time
- **S3 charges**: Storage for bundled site + rendered output
- **Typical cost**: A 30-second 1080p video costs roughly $0.01-0.05 depending on complexity
- **Concurrency**: AWS Lambda default concurrency limit is 1000 per region

## Limitations

- Requires AWS account with appropriate IAM permissions
- Lambda has a 15-minute execution timeout per invocation
- Maximum output file size limited by Lambda's `/tmp` storage (10GB)
- Cold starts can add 5-10 seconds to the first render

## Further Reference

See `tools/integrations/remotion.md` for the full CLI command reference including all Lambda subcommands.

Note: AWS infrastructure setup (IAM roles, S3 bucket policies, VPC configuration) is out of scope for this skill. Refer to the [Remotion Lambda documentation](https://www.remotion.dev/docs/lambda) for detailed AWS setup instructions.
