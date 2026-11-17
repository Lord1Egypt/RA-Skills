# Worker microservice template (`BackgroundService`)

Use for **Mode 3 (`add-worker`)**. One worker = one `.csproj`.

## `src/{{Solution}}.Workers.{{Worker}}/Program.cs`

```csharp
using {{Solution}}.Application;
using {{Solution}}.Infrastructure;
using {{Solution}}.Workers.{{Worker}};

var builder = Host.CreateApplicationBuilder(args);

builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);

builder.Services.AddHostedService<Worker>();

var host = builder.Build();
await host.RunAsync();
```

## `src/{{Solution}}.Workers.{{Worker}}/Worker.cs`

Choose **one** of the two `ExecuteAsync` bodies below based on the queue technology.

### Azure Service Bus (preferred for transactional queue workloads)

```csharp
using Azure.Messaging.ServiceBus;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace {{Solution}}.Workers.{{Worker}};

public sealed class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly ServiceBusClient _client;
    private readonly string _queueName;

    public Worker(ILogger<Worker> logger, IConfiguration config)
    {
        _logger = logger;
        var connString = config.GetConnectionString("ServiceBus")
            ?? throw new InvalidOperationException("ConnectionStrings:ServiceBus required.");
        _queueName = config["Worker:QueueName"]
            ?? throw new InvalidOperationException("Worker:QueueName required.");
        _client = new ServiceBusClient(connString);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await using var processor = _client.CreateProcessor(_queueName, new ServiceBusProcessorOptions
        {
            AutoCompleteMessages = false,
            MaxConcurrentCalls = 1
        });

        processor.ProcessMessageAsync += async args =>
        {
            try
            {
                _logger.LogInformation("Received message {Id}", args.Message.MessageId);

                // TODO: deserialize, call into Application service via DI scope, persist results.
                // Use args.CancellationToken (linked to stoppingToken).

                await args.CompleteMessageAsync(args.Message, args.CancellationToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to process message {Id}", args.Message.MessageId);
                await args.AbandonMessageAsync(args.Message, cancellationToken: args.CancellationToken);
            }
        };

        processor.ProcessErrorAsync += args =>
        {
            _logger.LogError(args.Exception, "Service Bus error from {Source}", args.ErrorSource);
            return Task.CompletedTask;
        };

        await processor.StartProcessingAsync(stoppingToken);
        await Task.Delay(Timeout.Infinite, stoppingToken);
        await processor.StopProcessingAsync(CancellationToken.None);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        await _client.DisposeAsync();
        await base.StopAsync(cancellationToken);
    }
}
```

### Azure Storage Queue (when there's no Service Bus)

```csharp
using Azure.Storage.Queues;
using Azure.Storage.Queues.Models;

protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    var queue = new QueueClient(_connectionString, _queueName);
    await queue.CreateIfNotExistsAsync(cancellationToken: stoppingToken);

    while (!stoppingToken.IsCancellationRequested)
    {
        QueueMessage[] messages = await queue.ReceiveMessagesAsync(maxMessages: 10, cancellationToken: stoppingToken);

        if (messages.Length == 0)
        {
            try { await Task.Delay(TimeSpan.FromSeconds(2), stoppingToken); }
            catch (TaskCanceledException) { break; }
            continue;
        }

        foreach (var msg in messages)
        {
            try
            {
                using var scope = _serviceProvider.CreateScope();
                // Resolve scoped services here, dispatch.
                await queue.DeleteMessageAsync(msg.MessageId, msg.PopReceipt, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Worker failed processing message {Id}", msg.MessageId);
                // Don't delete — let the queue re-deliver after the visibility timeout.
            }
        }
    }
}
```

Inject `IServiceProvider` to create a scope per message (so EF Core's scoped `AppDbContext` is fresh each iteration).

## `appsettings.json`

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "ConnectionStrings": {
    "Default": "",
    "ServiceBus": ""
  },
  "Worker": {
    "QueueName": ""
  }
}
```

## What the worker must **never** do

- `while (true) { ... Task.Delay(5s); }` without checking `stoppingToken` — breaks graceful shutdown.
- Resolve scoped services from the root provider — always create an `IServiceScope` per message.
- Reference `{{Solution}}.Api`. Workers depend on Application + Infrastructure only.
- Catch `Exception` and silently delete the message — that loses the failure forever.
