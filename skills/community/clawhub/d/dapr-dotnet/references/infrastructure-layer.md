# Infrastructure 层模板

> 摘自 dapr-dotnet 技能 v1.0.0「Infrastructure」章节。包含：BaseRepository 泛型仓储实现、TestRepository 示例。

## 一、BaseRepository.cs

```csharp
// Infrastructure/Repositories/BaseRepository.cs
public class BaseRepository<T> : SimpleClient<T>, IBaseRepository<T> where T : class, new()
{
    public BaseRepository(ISqlSugarClient context = null) : base(context)
    {
        base.Context = DbScoped.SugarScope;
    }

    /// <summary>
    /// 根据ID删除数据
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public async Task<bool> DeleteAsync(dynamic AId)
    {
        return await DeleteByIdAsync(AId);
    }

    /// <summary>
    /// 批量删除
    /// </summary>
    /// <param name="AIds"></param>
    /// <returns></returns>
    public async Task<bool> DeleteByIdsAsync(dynamic[] AIds)
    {
        return await base.DeleteByIdsAsync(AIds);
    }

    /// <summary>
    /// 根据ID查询数据
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public virtual async Task<T> FindAsync(dynamic AId)
    {
        return await GetByIdAsync(AId);
    }

    /// <summary>
    /// 根据ID查询
    /// </summary>
    /// <param name="AId"></param>
    /// <returns></returns>
    public async Task<T> FindAsync(Expression<Func<T, bool>> func)
    {
        return await GetSingleAsync(func);
    }

    /// <summary>
    /// 添加
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public async Task<bool> InsertAsync(T AEntity)
    {
        return await base.InsertAsync(AEntity);
    }

    /// <summary>
    /// 批量添加
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    public async Task<bool> InsertRangeAsync(List<T> AList)
    {
        return await base.InsertRangeAsync(AList);
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public List<T> Query()
    {
        return base.GetList();
    }

    /// <summary>
    /// 自定义查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public List<T> Query(Expression<Func<T, bool>> func)
    {
        return base.GetList(func);
    }

    /// <summary>
    /// 查询
    /// </summary>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync()
    {
        return await base.GetListAsync();
    }

    /// <summary>
    /// 自定义条件查询
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func)
    {
        return await base.GetListAsync(func);
    }

    /// <summary>
    /// 分页查询
    /// </summary>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(func).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="func"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> func, string orderByFields, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(func).OrderBy(orderByFields).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 自定义条件分页查询
    /// </summary>
    /// <param name="whereExpression"></param>
    /// <param name="orderByExpression"></param>
    /// <param name="order"></param>
    /// <param name="APageIndex"></param>
    /// <param name="APageSize"></param>
    /// <param name="ATotal"></param>
    /// <returns></returns>
    public async Task<List<T>> QueryAsync(Expression<Func<T, bool>> whereExpression, Expression<Func<T, object>> orderByExpression, OrderByType order, int APageIndex, int APageSize, RefAsync<int> ATotal)
    {
        return await base.Context.Queryable<T>().Where(whereExpression).OrderBy(orderByExpression, order).ToPageListAsync(APageIndex, APageSize, ATotal);
    }

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public async Task<bool> UpdateAsync(T AEntity)
    {
        return await base.UpdateAsync(AEntity);
    }

    /// <summary>
    /// 批量修改
    /// </summary>
    /// <param name="AList"></param>
    /// <returns></returns>
    public async Task<bool> UpdateRangeAsync(List<T> AList)
    {
        return await base.UpdateRangeAsync(AList);
    }

    /// <summary>
    /// 插入
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Insert(T AEntity)
    {
        return base.Insert(AEntity);
    }

    /// <summary>
    /// 删除
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Delete(T AEntity)
    {
        return base.Delete(AEntity);
    }

    /// <summary>
    /// 更新
    /// </summary>
    /// <param name="AEntity"></param>
    /// <returns></returns>
    public bool Update(T AEntity)
    {
        return base.Update(AEntity);
    }

    /// <summary>
    /// 查询数据
    /// </summary>
    /// <param name="func"></param>
    /// <returns></returns>
    public T Find(Expression<Func<T, bool>> func)
    {
        return base.GetFirst(func);
    }

    /// <summary>
    /// 开始事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void BeginTran()
    {
        base.Context.Ado.BeginTran();
    }

    /// <summary>
    /// 提交事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void CommitTran()
    {
        base.Context.Ado.CommitTran();
    }

    /// <summary>
    /// 回滚事务
    /// </summary>
    /// <exception cref="NotImplementedException"></exception>
    public void RollbackTran()
    {
        base.Context.Ado.RollbackTran();
    }

    #region 执行sql

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, object parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public DataTable GetDataTable(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataTable(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="ASql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string ASql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(ASql, parameters);
    }

    /// <summary>
    /// 获取DataTable数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataTable</returns>
    public async Task<DataTable> GetDataTableAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataTableAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, object parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public DataSet GetDataSetAll(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataSetAll(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataSet数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>DataSet</returns>
    public async Task<DataSet> GetDataSetAllAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataSetAllAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, object parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public IDataReader GetDataReader(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetDataReader(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取DataReader数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>IDataReader</returns>
    public async Task<IDataReader> GetDataReaderAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetDataReaderAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, object parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public object GetScalar(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.GetScalar(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, object parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 获取object数据
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>object</returns>
    public async Task<object> GetScalarAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.GetScalarAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommandWithGo(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.ExecuteCommandWithGo(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, object parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public int ExecuteCommand(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.ExecuteCommand(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, object parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行sql返回整型
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns>int</returns>
    public async Task<int> ExecuteCommandAsync(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.ExecuteCommandAsync(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, object parameters = null)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public List<T> SqlQuery<T>(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.SqlQuery<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, object parameters = null)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, List<SugarParameter> parameters)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public async Task<List<T>> SqlQueryAsync<T>(string sql, params SugarParameter[] parameters)
    {
        return await base.Context.Ado.SqlQueryAsync<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="sql"></param>
    /// <param name="whereObj"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, object whereObj = null)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, whereObj);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <param name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, params SugarParameter[] parameters)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, parameters);
    }

    /// <summary>
    /// 执行SQL返回自定义实体
    /// </summary>
    /// <typeparam name="T">实体对象</typeparam>
    /// <param name="sql"></param>
    /// <param name="parameters"></param>
    /// <returns></returns>
    public T SqlQuerySingle<T>(string sql, List<SugarParameter> parameters)
    {
        return base.Context.Ado.SqlQuerySingle<T>(sql, parameters);
    }

    #endregion
}

// Infrastructure/Repositories/TestRepository.cs
public class TestRepository : BaseRepository<Test>, ITestRepository
{
}
```

## 二、实现要点

1. **继承 SqlSugar `SimpleClient<T>`**：直接获得 `Insert/Update/Delete/GetList/GetByIdAsync` 等基础能力；构造函数中把 `base.Context` 固定为 `DbScoped.SugarScope`（作用域客户端，随 DI 作用域释放）。
2. **构造参数可选**：`ISqlSugarClient context = null`，便于单元测试时注入 mock。
3. **分页**：`base.Context.Queryable<T>()` + `ToPageListAsync(index, size, RefAsync<int> total)`，总记录数通过 `RefAsync<int>` 回传。
4. **事务**：`BeginTran/CommitTran/RollbackTran` 直接转发 `Context.Ado`，事务粒度由 Service 层控制（Service 调 `BeginTran` → 多个 Repository 操作 → `CommitTran`）。
5. **原生 SQL**：全部经 `Context.Ado`（DataTable / DataSet / DataReader / Scalar / ExecuteCommand / SqlQuery<T>），三种参数形态 `object` / `params SugarParameter[]` / `List<SugarParameter>`。
6. **新仓储零代码**：`XxxRepository : BaseRepository<Xxx>, IXxxRepository` 空类即可，DI 由 Autofac 程序集扫描自动注册。
