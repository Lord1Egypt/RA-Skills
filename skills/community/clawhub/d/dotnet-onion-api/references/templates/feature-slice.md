# Feature slice template — example entity `Customer`

Use this for **Mode 2 (`add-feature`)**. Substitute `Customer` → `{{Feature}}` and `Customers` → folder/plural form.

## 1. Domain — `src/{{Solution}}.Domain/Customers/Customer.cs`

```csharp
namespace {{Solution}}.Domain.Customers;

public sealed class Customer
{
    public int Id { get; private set; }
    public string Name { get; private set; } = default!;
    public string Email { get; private set; } = default!;
    public DateTime CreatedUtc { get; private set; }

    // EF needs a parameterless ctor; keep it private.
    private Customer() { }

    public Customer(string name, string email)
    {
        if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Name required.", nameof(name));
        if (string.IsNullOrWhiteSpace(email)) throw new ArgumentException("Email required.", nameof(email));

        Name = name.Trim();
        Email = email.Trim().ToLowerInvariant();
        CreatedUtc = DateTime.UtcNow;
    }

    public void Rename(string newName)
    {
        if (string.IsNullOrWhiteSpace(newName)) throw new ArgumentException("Name required.", nameof(newName));
        Name = newName.Trim();
    }
}
```

## 2. Application — port

`src/{{Solution}}.Application/Customers/ICustomerRepository.cs`

```csharp
using {{Solution}}.Domain.Customers;

namespace {{Solution}}.Application.Customers;

public interface ICustomerRepository
{
    Task<Customer?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct = default);
    Task AddAsync(Customer customer, CancellationToken ct = default);
    void Remove(Customer customer);
    Task<bool> EmailExistsAsync(string email, CancellationToken ct = default);
}
```

## 3. Application — DTOs

`src/{{Solution}}.Application/Customers/Dtos/CustomerDto.cs`

```csharp
namespace {{Solution}}.Application.Customers.Dtos;

public sealed record CustomerDto(int Id, string Name, string Email, DateTime CreatedUtc);

public sealed record CreateCustomerRequest(string Name, string Email);

public sealed record UpdateCustomerRequest(string Name);
```

## 4. Application — service + interface

`src/{{Solution}}.Application/Customers/ICustomerService.cs`

```csharp
using {{Solution}}.Application.Customers.Dtos;

namespace {{Solution}}.Application.Customers;

public interface ICustomerService
{
    Task<CustomerDto?> GetAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<CustomerDto>> ListAsync(CancellationToken ct = default);
    Task<CustomerDto> CreateAsync(CreateCustomerRequest req, CancellationToken ct = default);
    Task UpdateAsync(int id, UpdateCustomerRequest req, CancellationToken ct = default);
    Task DeleteAsync(int id, CancellationToken ct = default);
}
```

`src/{{Solution}}.Application/Customers/CustomerService.cs`

```csharp
using {{Solution}}.Application.Common;
using {{Solution}}.Application.Common.Exceptions;
using {{Solution}}.Application.Customers.Dtos;
using {{Solution}}.Domain.Customers;
using AutoMapper;

namespace {{Solution}}.Application.Customers;

public sealed class CustomerService : ICustomerService
{
    private readonly ICustomerRepository _repo;
    private readonly IUnitOfWork _uow;
    private readonly IMapper _mapper;

    public CustomerService(ICustomerRepository repo, IUnitOfWork uow, IMapper mapper)
    {
        _repo = repo;
        _uow = uow;
        _mapper = mapper;
    }

    public async Task<CustomerDto?> GetAsync(int id, CancellationToken ct = default)
    {
        var c = await _repo.GetByIdAsync(id, ct);
        return c is null ? null : _mapper.Map<CustomerDto>(c);
    }

    public async Task<IReadOnlyList<CustomerDto>> ListAsync(CancellationToken ct = default)
    {
        var list = await _repo.ListAsync(ct);
        return _mapper.Map<IReadOnlyList<CustomerDto>>(list);
    }

    public async Task<CustomerDto> CreateAsync(CreateCustomerRequest req, CancellationToken ct = default)
    {
        if (await _repo.EmailExistsAsync(req.Email, ct))
            throw new ConflictException($"Customer with email '{req.Email}' already exists.");

        var customer = new Customer(req.Name, req.Email);
        await _repo.AddAsync(customer, ct);
        await _uow.SaveChangesAsync(ct);

        return _mapper.Map<CustomerDto>(customer);
    }

    public async Task UpdateAsync(int id, UpdateCustomerRequest req, CancellationToken ct = default)
    {
        var customer = await _repo.GetByIdAsync(id, ct)
            ?? throw new NotFoundException(nameof(Customer), id);

        customer.Rename(req.Name);
        await _uow.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(int id, CancellationToken ct = default)
    {
        var customer = await _repo.GetByIdAsync(id, ct)
            ?? throw new NotFoundException(nameof(Customer), id);

        _repo.Remove(customer);
        await _uow.SaveChangesAsync(ct);
    }
}
```

## 5. Application — AutoMapper profile

`src/{{Solution}}.Application/Customers/Mapping/CustomerProfile.cs`

```csharp
using {{Solution}}.Application.Customers.Dtos;
using {{Solution}}.Domain.Customers;
using AutoMapper;

namespace {{Solution}}.Application.Customers.Mapping;

public sealed class CustomerProfile : Profile
{
    public CustomerProfile()
    {
        CreateMap<Customer, CustomerDto>();
    }
}
```

## 6. Infrastructure — EF configuration

`src/{{Solution}}.Infrastructure/Persistence/EntityConfigurations/CustomerConfiguration.cs`

```csharp
using {{Solution}}.Domain.Customers;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace {{Solution}}.Infrastructure.Persistence.EntityConfigurations;

public sealed class CustomerConfiguration : IEntityTypeConfiguration<Customer>
{
    public void Configure(EntityTypeBuilder<Customer> b)
    {
        b.ToTable("Customers");
        b.HasKey(x => x.Id);
        b.Property(x => x.Name).HasMaxLength(200).IsRequired();
        b.Property(x => x.Email).HasMaxLength(320).IsRequired();
        b.HasIndex(x => x.Email).IsUnique();
        b.Property(x => x.CreatedUtc).IsRequired();
    }
}
```

## 7. Infrastructure — repository adapter

`src/{{Solution}}.Infrastructure/Persistence/Repositories/CustomerRepository.cs`

```csharp
using {{Solution}}.Application.Customers;
using {{Solution}}.Domain.Customers;
using Microsoft.EntityFrameworkCore;

namespace {{Solution}}.Infrastructure.Persistence.Repositories;

public sealed class CustomerRepository : ICustomerRepository
{
    private readonly AppDbContext _db;
    public CustomerRepository(AppDbContext db) => _db = db;

    public Task<Customer?> GetByIdAsync(int id, CancellationToken ct = default) =>
        _db.Customers.FirstOrDefaultAsync(c => c.Id == id, ct);

    public async Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct = default) =>
        await _db.Customers.AsNoTracking().OrderBy(c => c.Name).ToListAsync(ct);

    public async Task AddAsync(Customer customer, CancellationToken ct = default) =>
        await _db.Customers.AddAsync(customer, ct);

    public void Remove(Customer customer) => _db.Customers.Remove(customer);

    public Task<bool> EmailExistsAsync(string email, CancellationToken ct = default) =>
        _db.Customers.AnyAsync(c => c.Email == email.ToLower(), ct);
}
```

Also register the DbSet on `AppDbContext`:

```csharp
public DbSet<Customer> Customers => Set<Customer>();
```

## 8. Api — controller

`src/{{Solution}}.Api/Controllers/CustomersController.cs`

```csharp
using {{Solution}}.Application.Common;
using {{Solution}}.Application.Customers;
using {{Solution}}.Application.Customers.Dtos;
using Microsoft.AspNetCore.Mvc;

namespace {{Solution}}.Api.Controllers;

public sealed class CustomersController : BaseController
{
    private readonly ICustomerService _service;

    public CustomersController(IUserContext userContext, ICustomerService service)
        : base(userContext)
    {
        _service = service;
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<CustomerDto>> Get(int id, CancellationToken ct)
    {
        var dto = await _service.GetAsync(id, ct);
        return dto is null ? NotFound() : Ok(dto);
    }

    [HttpGet]
    public async Task<ActionResult<IReadOnlyList<CustomerDto>>> List(CancellationToken ct) =>
        Ok(await _service.ListAsync(ct));

    [HttpPost]
    public async Task<ActionResult<CustomerDto>> Create([FromBody] CreateCustomerRequest req, CancellationToken ct)
    {
        var dto = await _service.CreateAsync(req, ct);
        return CreatedAtAction(nameof(Get), new { id = dto.Id }, dto);
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> Update(int id, [FromBody] UpdateCustomerRequest req, CancellationToken ct)
    {
        await _service.UpdateAsync(id, req, ct);
        return NoContent();
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        await _service.DeleteAsync(id, ct);
        return NoContent();
    }
}
```

## 9. Tests — `tests/{{Solution}}.UnitTests/Customers/CustomerServiceTests.cs`

```csharp
using {{Solution}}.Application.Common;
using {{Solution}}.Application.Common.Exceptions;
using {{Solution}}.Application.Customers;
using {{Solution}}.Application.Customers.Dtos;
using {{Solution}}.Application.Customers.Mapping;
using {{Solution}}.Domain.Customers;
using AutoMapper;
using FluentAssertions;
using NSubstitute;
using Xunit;

namespace {{Solution}}.UnitTests.Customers;

public class CustomerServiceTests
{
    private readonly ICustomerRepository _repo = Substitute.For<ICustomerRepository>();
    private readonly IUnitOfWork _uow = Substitute.For<IUnitOfWork>();
    private readonly IMapper _mapper;
    private readonly CustomerService _sut;

    public CustomerServiceTests()
    {
        var cfg = new MapperConfiguration(c => c.AddProfile<CustomerProfile>());
        _mapper = cfg.CreateMapper();
        _sut = new CustomerService(_repo, _uow, _mapper);
    }

    [Fact]
    public async Task CreateAsync_persists_and_returns_dto()
    {
        _repo.EmailExistsAsync("a@b.com", Arg.Any<CancellationToken>()).Returns(false);

        var dto = await _sut.CreateAsync(new CreateCustomerRequest("Alice", "a@b.com"));

        dto.Email.Should().Be("a@b.com");
        await _repo.Received(1).AddAsync(Arg.Any<Customer>(), Arg.Any<CancellationToken>());
        await _uow.Received(1).SaveChangesAsync(Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task CreateAsync_throws_when_email_exists()
    {
        _repo.EmailExistsAsync("a@b.com", Arg.Any<CancellationToken>()).Returns(true);

        var act = async () => await _sut.CreateAsync(new CreateCustomerRequest("Alice", "a@b.com"));

        await act.Should().ThrowAsync<ConflictException>();
    }
}
```
